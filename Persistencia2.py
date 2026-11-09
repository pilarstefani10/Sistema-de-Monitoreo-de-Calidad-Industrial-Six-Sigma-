from datetime import date
import json

from GestorArchivos import GestorArchivos
from Administrador import Administrador
from Profesional import Profesional
from Equipo import Equipo
from ProcedimientoDimensional import ProcedimientoDimensional
from ProcedimientoVisual import ProcedimientoVisual
from Lote import Lote
from Muestra import Muestra
from Inspeccion import Inspeccion
from Defecto import Defecto
from Reporte import Reporte


class Persistencia:
    # Se mantienen los encabezados del proyecto original.
    ENCABEZADOS = {
        "administradores.csv": ["id", "nombre"],
        "profesionales.csv": ["id", "nombre"],
        "certificaciones.csv": ["profesional_id", "nombre", "fecha_inicio", "fecha_vencimiento"],
        "equipos.csv": ["id", "categoria"],
        "calibraciones.csv": ["equipo_id", "fecha"],
        "procedimientos.csv": [
            "id", "tipo", "nombre", "categoria_equipo", "certificaciones_requeridas",
            "limite_gravedad", "valor_esperado", "tolerancia", "desvio",
            "rangos_gravedad", "probabilidad", "zonas_posibles", "descripciones"
        ],
        "lotes.csv": ["id", "cantidad_fabricada", "estado"],
        "muestras.csv": ["id", "lote_id", "unidades", "estado"],
        "inspecciones.csv": [
            "id", "muestra_id", "fecha", "profesional_id", "equipo_id",
            "procedimiento_id", "estado_inspeccion"
        ],
        "defectos.csv": ["muestra_id", "tipo", "gravedad", "descripcion"],
    }

    @classmethod
    def _leer(cls, archivo):
        ruta = GestorArchivos.CARPETA_DATOS / archivo
        filas = GestorArchivos.leer_csv_dict(ruta, cls.ENCABEZADOS[archivo])
        if filas is None:
            raise FileNotFoundError(f"No existe {ruta}")
        return filas

    @classmethod
    def _guardar(cls, archivo, filas):
        carpeta = GestorArchivos.CARPETA_DATOS
        carpeta.mkdir(parents=True, exist_ok=True)
        GestorArchivos.escribir_csv(carpeta / archivo, cls.ENCABEZADOS[archivo], filas)

    @staticmethod
    def verificar_ids(filas, objetos, nombre):
        """Comprueba que cada objeto recibió el ID de la fila correspondiente.

        IMPORTANTE: no reasigna IDs. Si hay saltos o filas reordenadas, falla.
        """
        if len(filas) != len(objetos):
            raise ValueError(f"Cantidad de {nombre} reconstruidos inconsistente")
        ids = list(map(lambda fila: fila["id"], filas))
        if len(ids) != len(set(ids)):
            raise ValueError(f"IDs duplicados en {nombre}.csv")
        for fila, objeto in zip(filas, objetos):
            if fila["id"] != objeto.getter_id():
                raise ValueError(
                    f"ID inconsistente en {nombre}: CSV={fila['id']}, "
                    f"objeto={objeto.getter_id()}. Verificá el orden y los contadores nextid."
                )

    @staticmethod
    def _registrar(objetos, registrar):
        # Se usa for aquí porque registrar() tiene efectos secundarios.
        for objeto in objetos:
            registrar(objeto)

    @staticmethod
    def _crear_procedimiento(fila):
        datos = {
            "nombre": fila["nombre"],
            "categoria_equipo_requerida": fila["categoria_equipo"],
            "certificaciones_requeridas": set(json.loads(fila["certificaciones_requeridas"])),
            "limite_gravedad": int(fila["limite_gravedad"]),
        }
        if fila["tipo"].lower() == "dimensional":
            datos.update({
                "valor_esperado": float(fila["valor_esperado"]),
                "tolerancia": float(fila["tolerancia"]),
                "desvio": float(fila["desvio"]),
                "rangos_gravedad": json.loads(fila["rangos_gravedad"]),
            })
            return ProcedimientoDimensional(**datos)
        if fila["tipo"].lower() == "visual":
            datos.update({
                "probabilidad": float(fila["probabilidad"]),
                "zonas_posibles": json.loads(fila["zonas_posibles"]),
                "descripciones": json.loads(fila["descripciones"]),
            })
            return ProcedimientoVisual(**datos)
        raise ValueError(f"Tipo de procedimiento desconocido: {fila['tipo']}")

    @staticmethod
    def _crear_inspeccion(fila, empresa, muestras):
        muestra = muestras[fila["muestra_id"]]
        # Inspeccion.__init__ valida contra la situación presente del equipo
        # y profesional. Para recuperar hechos históricos conservamos desde_archivo().
        inspeccion = Inspeccion.desde_archivo(
            fila["id"],
            date.fromisoformat(fila["fecha"]),
            empresa.buscar_profesional(fila["profesional_id"]),
            empresa.buscar_equipo(fila["equipo_id"]),
            empresa.buscar_procedimiento(fila["procedimiento_id"]),
            muestra,
        )
        return inspeccion
    
    @staticmethod
    def _restaurar_muestra(muestra, estado):
        inspeccion = muestra.getter_inspeccion()
        if estado == "PENDIENTE":
            if muestra.getter_defectos():
                raise ValueError("Una muestra pendiente tiene defectos: " + muestra.getter_id())
        elif estado in ("CONFORME", "NO_CONFORME"):
            if inspeccion is None:
                raise ValueError("Muestra cerrada sin inspección: " + muestra.getter_id())
            resultado = "CONFORME" if inspeccion.conformidad() else "NO_CONFORME"
            if estado != resultado:
                raise ValueError("Estado y defectos incompatibles: " + muestra.getter_id())
        else:
            raise ValueError("Estado de muestra inválido: " + estado)
        muestra.restaurar_estado(estado)

    @staticmethod
    def _restaurar_inspeccion(inspeccion, estado):
        profesional = inspeccion.getter_profesional()
        muestra = inspeccion.getter_muestra()
        if estado == "PENDIENTE":
            profesional.asignar_inspeccion(inspeccion)
        elif estado == "REPORTE_PENDIENTE":
            profesional.restaurar_reporte_pendiente(inspeccion)
        elif estado == "FINALIZADA":
            if muestra.getter_estado() == "NO_CONFORME":
                reporte = Reporte(inspeccion.getter_id() + "R", inspeccion)
                inspeccion.registrar_reporte(reporte)
            elif muestra.getter_estado() != "CONFORME":
                raise ValueError("Inspección finalizada con muestra pendiente")
            profesional.restaurar_inspeccion_finalizada(inspeccion)
        else:
            raise ValueError("Estado de inspección inválido: " + estado)
        
    @staticmethod
    def _restaurar_lote(lote, estado):
        if estado in ("APROBADO", "RECHAZADO"):
            if lote.resultado_segun_criterio() != estado:
                raise ValueError("Estado incompatible para lote " + lote.getter_id())
        lote.restaurar_estado(estado)

        
    @staticmethod
    def _restaurar_defecto(fila, muestras):
        defecto = Defecto(
            fila["tipo"],
            int(fila["gravedad"]),
            fila["descripcion"]
        )

        muestra = muestras[fila["muestra_id"]]
        muestra.restaurar_defecto(defecto)

    def cargar_estado_total(self, empresa):
        # 1. Administradores (su __init__ registra automáticamente en Empresa).
        filas = self._leer("administradores.csv")
        administradores = list(map(lambda f: Administrador(f["nombre"], empresa), filas))
        self.verificar_ids(filas, administradores, "administradores")

        # 2. Profesionales.
        filas = self._leer("profesionales.csv")
        profesionales = list(map(lambda f: Profesional(f["nombre"]), filas))
        self.verificar_ids(filas, profesionales, "profesionales")
        self._registrar(profesionales, empresa.registrar_profesional)

        # 3. Certificaciones

        for fila in self._leer("certificaciones.csv"):

            profesional = empresa.buscar_profesional(
                fila["profesional_id"]
            )

            profesional.agregar_certificacion(
                fila["nombre"],
                date.fromisoformat(fila["fecha_inicio"]),
                date.fromisoformat(fila["fecha_vencimiento"])
            )

        # 4. Equipos.
        filas = self._leer("equipos.csv")
        equipos = list(map(lambda f: Equipo(f["categoria"]), filas))
        self.verificar_ids(filas, equipos, "equipos")
        self._registrar(equipos, empresa.registrar_equipo)

        # 5. Calibraciones (se conserva historial completo).

        for fila in self._leer("calibraciones.csv"):

            equipo = empresa.buscar_equipo(fila["equipo_id"])

            equipo.calibrar(
                date.fromisoformat(fila["fecha"])
            )
        # 6. Procedimientos.
        filas = self._leer("procedimientos.csv")
        procedimientos = list(map(self._crear_procedimiento, filas))
        self.verificar_ids(filas, procedimientos, "procedimientos")
        self._registrar(procedimientos, empresa.registrar_procedimiento)

        # 7. Lotes.
        filas = self._leer("lotes.csv")
        lotes = list(map(lambda f: Lote(int(f["cantidad_fabricada"])), filas))
        self.verificar_ids(filas, lotes, "lotes")
        self._registrar(
            lotes,
            lambda lote: empresa.registrar_lote(lote, False)
        )
        estados_lotes = {f["id"]: f["estado"] for f in filas}
        empresa.reconstruir_arbol_lotes()

        # 8. Muestras: el __init__ sí recibe su ID como argumento.
        muestras = {}
        estados_muestras = {}

        for fila in self._leer("muestras.csv"):

            lote = empresa.buscar_lote(fila["lote_id"])

            muestra = Muestra(
                fila["id"],
                int(fila["unidades"]),
                lote
            )

            if muestra.getter_id() != lote.proximo_id_muestra():
                raise ValueError(
                    "ID u orden de muestra inconsistente: " + fila["id"]
                )

            if muestra.getter_id() in muestras:
                raise ValueError(
                    "ID de muestra duplicado: " + fila["id"]
                )

            lote.agregar_muestra(muestra)

            muestras[muestra.getter_id()] = muestra
            estados_muestras[muestra.getter_id()] = fila["estado"]

        # 9. Inspecciones históricas.
        filas = self._leer("inspecciones.csv")
        inspecciones = list(map(lambda f: self._crear_inspeccion(f, empresa, muestras), filas))
        self.verificar_ids(filas, inspecciones, "inspecciones")
        for inspeccion in inspecciones:
            muestra = inspeccion.getter_muestra()
            if inspeccion.getter_id() != muestra.getter_id() + "I":
                raise ValueError("ID de inspección inconsistente")
            muestra.setter_inspeccion(inspeccion)
        if any(map(lambda m: m.getter_inspeccion() is None, muestras.values())):
            raise ValueError("Hay muestras sin inspección asignada")

        # 10. Defectos: crear objetos sin evaluar nuevamente.
        for fila in self._leer("defectos.csv"):
            self._restaurar_defecto(fila, muestras)

        # 11. Estados y colas / pilas profesionales.
        for muestra in muestras.values():
            self._restaurar_muestra(muestra, estados_muestras[muestra.getter_id()])
        for fila, inspeccion in zip(filas, inspecciones):
            self._restaurar_inspeccion(inspeccion, fila["estado_inspeccion"])

        # 12. Estados finales de lotes.
        for lote in lotes:
            self._restaurar_lote(lote, estados_lotes[lote.getter_id()])

    @staticmethod
    def _filas_asociadas(contenedores, obtener_elementos, obtener_id):
        """Aplana objetos dependientes agregándoles la columna de su dueño."""
        return [
            {**elemento.estandarizar(), **{obtener_id: contenedor.getter_id()}}
            for contenedor in contenedores
            for elemento in obtener_elementos(contenedor)
        ]

    def guardar_estado_total(self, empresa):
        profesionales = empresa.getter_profesionales()
        equipos = empresa.getter_equipos()
        lotes = empresa.getter_lotes()
        procedimientos = empresa.getter_procedimientos()
        muestras = [m for lote in lotes for m in lote.getter_muestras()]

        # Cada estandarizar() devuelve un diccionario compatible con DictWriter.
        self._guardar("administradores.csv", map(lambda a: a.estandarizar(), empresa.getter_administradores()))
        self._guardar("profesionales.csv", map(lambda p: p.estandarizar(), profesionales))
        self._guardar("certificaciones.csv", self._filas_asociadas(
            profesionales, lambda p: p.getter_certificaciones(), "profesional_id"))
        self._guardar("equipos.csv", map(lambda e: e.estandarizar(), equipos))
        self._guardar("calibraciones.csv", (
            {"equipo_id": e.getter_id(), "fecha": fecha.isoformat()}
            for e in equipos for fecha in e.getter_calibraciones()
        ))
        self._guardar("procedimientos.csv", map(lambda p: p.estandarizar(), procedimientos))

        for muestra in muestras:
            inspeccion = muestra.getter_inspeccion()
            if inspeccion is not None and inspeccion.getter_reporte() is not None:
                reporte = inspeccion.getter_reporte()
                GestorArchivos.guardar_reporte(reporte.getter_id(), reporte.crear_resumen())

        self._guardar("lotes.csv", map(lambda l: l.estandarizar(), lotes))
        self._guardar("muestras.csv", map(lambda m: m.estandarizar(), muestras))
        self._guardar("defectos.csv", self._filas_asociadas(
            muestras, lambda m: m.getter_defectos(), "muestra_id"))

        # Conservar el orden original de pila (invertido al escribir) y cola (FIFO).
        # Inspecciones finalizadas
        finalizadas = []
        pendientes = []

        for profesional in profesionales:
            for inspeccion in reversed(profesional.getter_historial()):
                finalizadas.append(inspeccion)

            pendientes.extend(
                profesional.getter_inspecciones_pendientes()
            )

        self._guardar(
            "inspecciones.csv",
            map(
                lambda inspeccion: self._serializar_inspeccion(
                    inspeccion, finalizadas
                ),
                pendientes + finalizadas
            )
        )
    
    @staticmethod
    def _serializar_inspeccion(inspeccion, finalizadas):
        fila = inspeccion.estandarizar()

        if inspeccion in finalizadas:
            estado = "FINALIZADA"

        elif inspeccion.getter_muestra().getter_estado() == "NO_CONFORME":
            estado = "REPORTE_PENDIENTE"

        else:
            estado = "PENDIENTE"

        fila["estado_inspeccion"] = estado

        return fila

