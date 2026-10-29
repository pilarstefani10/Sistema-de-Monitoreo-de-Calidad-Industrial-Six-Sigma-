from Excepciones import DatosInvalidosError
from Profesional import Profesional
from datetime import date
from pathlib import Path
import json
from GestorArchivos import GestorArchivos
from Administrador import Administrador
from Profesional import Profesional
from Equipo import Equipo
from Procedimiento import Procedimiento
from ProcedimientoDimensional import ProcedimientoDimensional
from ProcedimientoVisual import ProcedimientoVisual
from Lote import Lote
from Muestra import Muestra
from Inspeccion import Inspeccion
from Defecto import Defecto
from Reporte import Reporte
class Empresa:
#La idea es que haya una única empresa o instancia que funcionará como un repertorio universal donde se añaden todos los profesionales, lotes, procedimientos, equipos y certificaciones
    def __init__(self, nombre):
        if not nombre:
            raise DatosInvalidosError("El nombre no puede estar vacío")

        self.__nombre = nombre
        self.__lotes = {}#Combiene más en diccionarios separados porque sino sería un diccionarios con listas
        self.__profesionales = {}#Y perdería sentido
        self.__equipos = {}
        self.__procedimientos = {}
        self.__administradores = {}

    def registrar_lote(self, lote):
        if lote.getter_id() in self.__lotes:
            raise DatosInvalidosError("ID de lote duplicado")

        self.__lotes[lote.getter_id()] = lote

    def registrar_profesional(self, profesional):
        if profesional.getter_id() in self.__profesionales:
            raise DatosInvalidosError("ID de profesional duplicado")

        self.__profesionales[profesional.getter_id()] = profesional
        

    def registrar_administrador(self, administrador):
        if administrador.getter_id() in self.__administradores:
            raise DatosInvalidosError("ID de administrador duplicado")

        self.__administradores[administrador.getter_id()] = administrador

    def registrar_equipo(self, equipo):
        if equipo.getter_id() in self.__equipos:
            raise DatosInvalidosError("ID de equipo duplicado")

        self.__equipos[equipo.getter_id()] = equipo

    def registrar_procedimiento(self, procedimiento):
        if procedimiento.getter_id() in self.__procedimientos:
            raise DatosInvalidosError("ID de procedimiento duplicado")

        self.__procedimientos[procedimiento.getter_id()] = procedimiento

    @staticmethod
    def buscar(diccionario, ID, tipo):
        if ID not in diccionario:
            raise DatosInvalidosError("No existe un " + tipo + " con el ID " + str(ID) + ".")
        return diccionario[ID]

    def buscar_lote(self, ID):
        return Empresa.buscar(self.__lotes, ID, "lote")

    def buscar_profesional(self, ID):
        return Empresa.buscar(self.__profesionales, ID, "profesional")

    def buscar_equipo(self, ID):
        return Empresa.buscar(self.__equipos, ID, "equipo")

    def buscar_procedimiento(self, ID):
        return Empresa.buscar(self.__procedimientos, ID, "procedimiento")

    def getter_equipos(self):
        return list(self.__equipos.values())

    def getter_lotes(self):
        return list(self.__lotes.values())

    def getter_profesionales(self):
        return list(self.__profesionales.values())

    def getter_procedimientos(self):
        return list(self.__procedimientos.values())

    def buscar_empleado(self, nombre, ID):
        if ID in self.__profesionales:
            empleado = self.__profesionales[ID]
        elif ID in self.__administradores:
            empleado = self.__administradores[ID]
        else:
            raise DatosInvalidosError("No existe un empleado con el ID " + str(ID) + ".")

        if empleado.getter_nombre() != nombre:
            raise DatosInvalidosError("El nombre no coincide con el ID ingresado.")

        return empleado

    
    @staticmethod
    def _leer(nombre_archivo):
        ruta = Path("datos") / nombre_archivo
        filas = GestorArchivos.leer_csv_dict(ruta)

        if filas is None:
            raise FileNotFoundError(f"No existe {ruta}")

        return filas


    @staticmethod
    def _guardar(nombre_archivo, encabezados, filas):
        carpeta = Path("datos")
        carpeta.mkdir(parents=True, exist_ok=True)

        GestorArchivos.escribir_csv(
            carpeta / nombre_archivo,
            encabezados,
            filas
        )


    @staticmethod
    def _crear_con_id(tipo, contador, ID, prefijo, *args, **kwargs):
        numero = ID[len(prefijo):]

        if not ID.startswith(prefijo) or not numero.isdigit() or int(numero) <= 0:
            raise ValueError(f"ID inválido: {ID}")

        siguiente = contador.nextid
        contador.nextid = int(numero)

        try:
            objeto = tipo(*args, **kwargs)

            if objeto.getter_id() != ID:
                raise ValueError(f"No se pudo recuperar el ID {ID}")

            return objeto
        finally:
            contador.nextid = max(siguiente, contador.nextid)



    def getter_administradores(self):
        return list(self.__administradores.values())


    
    def cargar_estado_total(self):

        # 1. Administradores
        for fila in self._leer("administradores.csv"):
            self._crear_con_id(
                Administrador, Administrador,
                fila["id"], "A",
                fila["nombre"], self
            )

        # 2. Profesionales
        for fila in self._leer("profesionales.csv"):
            profesional = self._crear_con_id(
                Profesional, Profesional,
                fila["id"], "P",
                fila["nombre"]
            )
            self.registrar_profesional(profesional)

        # 3. Certificaciones
        for fila in self._leer("certificaciones.csv"):
            profesional = self.buscar_profesional(
                fila["profesional_id"]
            )
            profesional.agregar_certificacion(
                fila["nombre"],
                date.fromisoformat(fila["fecha_inicio"]),
                date.fromisoformat(fila["fecha_vencimiento"])
            )

        # 4. Equipos
        for fila in self._leer("equipos.csv"):
            equipo = self._crear_con_id(
                Equipo, Equipo,
                fila["id"], "E",
                fila["categoria"]
            )
            self.registrar_equipo(equipo)

        # 5. Historial de calibraciones
        for fila in self._leer("calibraciones.csv"):
            equipo = self.buscar_equipo(fila["equipo_id"])
            equipo.calibrar(date.fromisoformat(fila["fecha"]))

        # 6. Procedimientos
        for fila in self._leer("procedimientos.csv"):
            datos = {
                "nombre": fila["nombre"],
                "categoria_equipo_requerida": fila["categoria_equipo"],
                "certificaciones_requeridas": set(
                    json.loads(fila["certificaciones_requeridas"])
                ),
                "limite_gravedad": int(fila["limite_gravedad"])
            }

            if fila["tipo"].lower() == "dimensional":
                tipo = ProcedimientoDimensional
                datos.update({
                    "valor_esperado": float(fila["valor_esperado"]),
                    "tolerancia": float(fila["tolerancia"]),
                    "desvio": float(fila["desvio"]),
                    "rangos_gravedad": json.loads(
                        fila["rangos_gravedad"]
                    )
                })

            elif fila["tipo"].lower() == "visual":
                tipo = ProcedimientoVisual
                datos.update({
                    "probabilidad": float(fila["probabilidad"]),
                    "zonas_posibles": json.loads(fila["zonas_posibles"]),
                    "descripciones": json.loads(fila["descripciones"])
                })

            else:
                raise ValueError("Tipo de procedimiento desconocido")

            procedimiento = self._crear_con_id(
                tipo, Procedimiento,
                fila["id"], "PR",
                **datos
            )
            self.registrar_procedimiento(procedimiento)

        # 7. Lotes
        estados_lotes = {}

        for fila in self._leer("lotes.csv"):
            lote = self._crear_con_id(
                Lote, Lote,
                fila["id"], "L",
                int(fila["cantidad_fabricada"])
            )
            self.registrar_lote(lote)
            estados_lotes[lote.getter_id()] = fila["estado"]

        # 8. Muestras
        muestras = {}
        estados_muestras = {}

        for fila in self._leer("muestras.csv"):
            lote = self.buscar_lote(fila["lote_id"])

            muestra = Muestra(
                fila["id"],
                int(fila["unidades"]),
                lote
            )

            lote.agregar_muestra(muestra)
            muestras[muestra.getter_id()] = muestra
            estados_muestras[muestra.getter_id()] = fila["estado"]

        # 9. Inspecciones
        for fila in self._leer("inspecciones.csv"):
            muestra = muestras[fila["muestra_id"]]
            profesional = self.buscar_profesional(
                fila["profesional_id"]
            )
            equipo = self.buscar_equipo(fila["equipo_id"])
            procedimiento = self.buscar_procedimiento(
                fila["procedimiento_id"]
            )

            if fila["id"] != muestra.getter_id() + "I":
                raise ValueError("ID de inspección inconsistente")

            inspeccion = Inspeccion.desde_archivo(
                fila["id"],
                date.fromisoformat(fila["fecha"]),
                profesional,
                equipo,
                procedimiento,
                muestra
            )

            muestra.setter_inspeccion(inspeccion)

            if estados_muestras[muestra.getter_id()] == "PENDIENTE":
                profesional.asignar_inspeccion(inspeccion)

        # 10. Defectos
        for fila in self._leer("defectos.csv"):
            muestra = muestras[fila["muestra_id"]]

            defecto = Defecto(
                fila["tipo"],
                int(fila["gravedad"]),
                fila["descripcion"]
            )

            muestra.registrar_defectos([defecto])

        # 11. Restaurar los estados de las muestras
        for ID, muestra in muestras.items():
            muestra.restaurar_estado(estados_muestras[ID])

            if muestra.getter_estado() == "NO_CONFORME":
                inspeccion = muestra.getter_inspeccion()

                if inspeccion is not None:
                    reporte = Reporte(
                        inspeccion.getter_id() + "R",
                        inspeccion
                    )
                    inspeccion.registrar_reporte(reporte)

        # 12. Restaurar los estados de los lotes
        for lote in self.getter_lotes():
            lote.restaurar_estado(
                estados_lotes[lote.getter_id()]
            )

    
    def guardar_estado_total(self):

        # Administradores
        self._guardar(
            "administradores.csv",
            ["id", "nombre"],
            [
                {
                    "id": a.getter_id(),
                    "nombre": a.getter_nombre()
                }
                for a in self.getter_administradores()
            ]
        )

        # Profesionales
        self._guardar(
            "profesionales.csv",
            ["id", "nombre"],
            [
                {
                    "id": p.getter_id(),
                    "nombre": p.getter_nombre()
                }
                for p in self.getter_profesionales()
            ]
        )

        # Certificaciones
        filas = []

        for p in self.getter_profesionales():
            for c in p.getter_certificaciones():
                filas.append({
                    "profesional_id": p.getter_id(),
                    "nombre": c.getter_nombre(),
                    "fecha_inicio": c.getter_fecha_inicio().isoformat(),
                    "fecha_vencimiento": c.getter_fecha_vencimiento().isoformat()
                })

        self._guardar(
            "certificaciones.csv",
            ["profesional_id", "nombre", "fecha_inicio", "fecha_vencimiento"],
            filas
        )

        # Equipos y calibraciones
        equipos = []
        calibraciones = []

        for e in self.getter_equipos():
            equipos.append({
                "id": e.getter_id(),
                "categoria": e.getter_categoria()
            })

            for fecha in e.getter_calibraciones():
                calibraciones.append({
                    "equipo_id": e.getter_id(),
                    "fecha": fecha.isoformat()
                })

        self._guardar("equipos.csv", ["id", "categoria"], equipos)
        self._guardar(
            "calibraciones.csv",
            ["equipo_id", "fecha"],
            calibraciones
        )

        # Procedimientos
        filas = []

        for p in self.getter_procedimientos():
            fila = {
                "id": p.getter_id(),
                "tipo": "",
                "nombre": p.getter_nombre(),
                "categoria_equipo": p.getter_categoria_equipo(),
                "certificaciones_requeridas": json.dumps(
                    sorted(p.getter_certificaciones_requeridas()),
                    ensure_ascii=False
                ),
                "limite_gravedad": p.getter_limitegravedad(),
                "valor_esperado": "",
                "tolerancia": "",
                "desvio": "",
                "rangos_gravedad": "",
                "probabilidad": "",
                "zonas_posibles": "",
                "descripciones": ""
            }

            if isinstance(p, ProcedimientoDimensional):
                fila["tipo"] = "dimensional"
                fila["valor_esperado"] = p.getter_valor_esperado()
                fila["tolerancia"] = p.getter_tolerancia()
                fila["desvio"] = p.getter_desvio()
                fila["rangos_gravedad"] = json.dumps(
                    p.getter_rangos_gravedad(),
                    ensure_ascii=False
                )

            elif isinstance(p, ProcedimientoVisual):
                fila["tipo"] = "visual"
                fila["probabilidad"] = p.getter_probabilidad()
                fila["zonas_posibles"] = json.dumps(
                    p.getter_zonas_posibles(),
                    ensure_ascii=False
                )
                fila["descripciones"] = json.dumps(
                    p.getter_descripciones(),
                    ensure_ascii=False
                )

            filas.append(fila)

        encabezados = [
            "id", "tipo", "nombre", "categoria_equipo",
            "certificaciones_requeridas", "limite_gravedad",
            "valor_esperado", "tolerancia", "desvio",
            "rangos_gravedad", "probabilidad",
            "zonas_posibles", "descripciones"
        ]

        self._guardar("procedimientos.csv", encabezados, filas)

        # Lotes, muestras y defectos
        lotes = []
        muestras = []
        defectos = []
        inspecciones_terminadas = []

        for lote in self.getter_lotes():
            lotes.append({
                "id": lote.getter_id(),
                "cantidad_fabricada": lote.getter_cantidad_fabricada(),
                "estado": lote.getter_estado()
            })

            for muestra in lote.getter_muestras():
                muestras.append({
                    "id": muestra.getter_id(),
                    "lote_id": lote.getter_id(),
                    "unidades": muestra.getter_unidadesrepresentadas(),
                    "estado": muestra.getter_estado()
                })

                for defecto in muestra.getter_defectos():
                    defectos.append({
                        "muestra_id": muestra.getter_id(),
                        "tipo": defecto.getter_tipo(),
                        "gravedad": defecto.getter_gravedad(),
                        "descripcion": defecto.getter_descripcion()
                    })

                inspeccion = muestra.getter_inspeccion()

                if inspeccion is not None:
                    if muestra.getter_estado() != "PENDIENTE":
                        inspecciones_terminadas.append(inspeccion)

        self._guardar(
            "lotes.csv",
            ["id", "cantidad_fabricada", "estado"],
            lotes
        )

        self._guardar(
            "muestras.csv",
            ["id", "lote_id", "unidades", "estado"],
            muestras
        )

        self._guardar(
            "defectos.csv",
            ["muestra_id", "tipo", "gravedad", "descripcion"],
            defectos
        )

        # Inspecciones: las pendientes se guardan en orden FIFO
        pendientes = []

        for profesional in self.getter_profesionales():
            pendientes.extend(
                profesional.getter_inspecciones_pendientes()
            )

        filas = []

        for i in pendientes + inspecciones_terminadas:
            filas.append({
                "id": i.getter_id(),
                "muestra_id": i.getter_muestra().getter_id(),
                "fecha": i.getter_fecha().isoformat(),
                "profesional_id": i.getter_profesional().getter_id(),
                "equipo_id": i.getter_equipo().getter_id(),
                "procedimiento_id": i.getter_procedimiento().getter_id()
            })

        self._guardar(
            "inspecciones.csv",
            [
                "id", "muestra_id", "fecha",
                "profesional_id", "equipo_id", "procedimiento_id"
            ],
            filas
        )


        