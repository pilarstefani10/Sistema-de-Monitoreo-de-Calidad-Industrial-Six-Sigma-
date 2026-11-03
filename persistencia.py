from datetime import date
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


class Persistencia:

    @staticmethod
    def _leer(nombre_archivo):

        encabezados_csv = {
            "administradores.csv": ["id", "nombre"],
            "profesionales.csv": ["id", "nombre"],
            "certificaciones.csv": [
                "profesional_id", "nombre",
                "fecha_inicio", "fecha_vencimiento"
            ],
            "equipos.csv": ["id", "categoria"],
            "calibraciones.csv": ["equipo_id", "fecha"],
            "procedimientos.csv": [
                "id", "tipo", "nombre", "categoria_equipo",
                "certificaciones_requeridas", "limite_gravedad",
                "valor_esperado", "tolerancia", "desvio",
                "rangos_gravedad", "probabilidad",
                "zonas_posibles", "descripciones"
            ],
            "lotes.csv": [
                "id", "cantidad_fabricada", "estado"
            ],
            "muestras.csv": [
                "id", "lote_id", "unidades", "estado"
            ],
            "inspecciones.csv": [
                "id", "muestra_id", "fecha",
                "profesional_id", "equipo_id",
                "procedimiento_id"
            ],
            "defectos.csv": [
                "muestra_id", "tipo",
                "gravedad", "descripcion"
            ]
        }

        ruta = GestorArchivos.CARPETA_DATOS / nombre_archivo

        filas = GestorArchivos.leer_csv_dict(
            ruta, encabezados_csv[nombre_archivo]
        )

        if filas is None:
            raise FileNotFoundError(f"No existe {ruta}")

        return filas

    @staticmethod
    def _guardar(nombre_archivo, encabezados, filas):

        carpeta = GestorArchivos.CARPETA_DATOS
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

    def cargar_estado_total(self, empresa):

        # 1. Administradores
        for fila in self._leer("administradores.csv"):
            self._crear_con_id(
                Administrador, Administrador,
                fila["id"], "A",
                fila["nombre"], empresa
            )

        # 2. Profesionales
        for fila in self._leer("profesionales.csv"):
            profesional = self._crear_con_id(
                Profesional, Profesional,
                fila["id"], "P",
                fila["nombre"]
            )

            empresa.registrar_profesional(profesional)

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

        # 4. Equipos
        for fila in self._leer("equipos.csv"):

            equipo = self._crear_con_id(
                Equipo, Equipo,
                fila["id"], "E",
                fila["categoria"]
            )

            empresa.registrar_equipo(equipo)

        # 5. Historial de calibraciones
        for fila in self._leer("calibraciones.csv"):

            equipo = empresa.buscar_equipo(
                fila["equipo_id"]
            )

            equipo.calibrar(
                date.fromisoformat(fila["fecha"])
            )

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
                    "zonas_posibles": json.loads(
                        fila["zonas_posibles"]
                    ),
                    "descripciones": json.loads(
                        fila["descripciones"]
                    )
                })

            else:
                raise ValueError("Tipo de procedimiento desconocido")

            procedimiento = self._crear_con_id(
                tipo, Procedimiento,
                fila["id"], "PR",
                **datos
            )

            empresa.registrar_procedimiento(procedimiento)

        # 7. Lotes
        estados_lotes = {}

        for fila in self._leer("lotes.csv"):

            lote = self._crear_con_id(
                Lote, Lote,
                fila["id"], "L",
                int(fila["cantidad_fabricada"])
            )

            empresa.registrar_lote(lote)
            estados_lotes[lote.getter_id()] = fila["estado"]

        empresa.reconstruir_arbol_lotes()

        # 8. Muestras
        muestras = {}
        estados_muestras = {}

        for fila in self._leer("muestras.csv"):

            lote = empresa.buscar_lote(
                fila["lote_id"]
            )

            muestra = Muestra(
                fila["id"],
                int(fila["unidades"]),
                lote
            )

            lote.agregar_muestra(muestra)

            muestras[muestra.getter_id()] = muestra
            estados_muestras[muestra.getter_id()] = fila["estado"]

        # 9. Inspecciones
        inspecciones_finalizadas = []

        for fila in self._leer("inspecciones.csv"):

            muestra = muestras[fila["muestra_id"]]

            profesional = empresa.buscar_profesional(
                fila["profesional_id"]
            )

            equipo = empresa.buscar_equipo(
                fila["equipo_id"]
            )

            procedimiento = empresa.buscar_procedimiento(
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

            elif estados_muestras[muestra.getter_id()] in (
                "CONFORME", "NO_CONFORME"
            ):
                inspecciones_finalizadas.append(inspeccion)

        # 10. Defectos
        for fila in self._leer("defectos.csv"):

            muestra = muestras[fila["muestra_id"]]

            defecto = Defecto(
                fila["tipo"],
                int(fila["gravedad"]),
                fila["descripcion"]
            )

            muestra.restaurar_defecto(defecto)

        # 11. Restaurar estados de muestras
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

        # Restaurar historial de inspecciones finalizadas
        for inspeccion in inspecciones_finalizadas:

            profesional = inspeccion.getter_profesional()

            profesional.restaurar_inspeccion_finalizada(
                inspeccion
            )

        # 12. Restaurar estados de los lotes
        for lote in empresa.getter_lotes():

            lote.restaurar_estado(
                estados_lotes[lote.getter_id()]
            )
