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
                "procedimiento_id", "estado_inspeccion"
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
        inspecciones_recuperadas = []

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

            estado = fila["estado_inspeccion"]

            if estado not in (
                "PENDIENTE",
                "REPORTE_PENDIENTE",
                "FINALIZADA"
            ):
                raise ValueError("Estado de inspección inválido")

            inspeccion = Inspeccion.desde_archivo(
                fila["id"],
                date.fromisoformat(fila["fecha"]),
                profesional,
                equipo,
                procedimiento,
                muestra
            )

            muestra.setter_inspeccion(inspeccion)

            inspecciones_recuperadas.append(
                (inspeccion, estado)
            )


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

        # Restaurar inspecciones según su estado guardado
        for inspeccion, estado in inspecciones_recuperadas:

            profesional = inspeccion.getter_profesional()
            muestra = inspeccion.getter_muestra()

            if estado == "PENDIENTE":
                profesional.asignar_inspeccion(inspeccion)

            elif estado == "REPORTE_PENDIENTE":
                profesional.restaurar_reporte_pendiente(
                    inspeccion
                )

            elif estado == "FINALIZADA":

                if muestra.getter_estado() == "NO_CONFORME":
                    reporte = Reporte(
                        inspeccion.getter_id() + "R",
                        inspeccion
                    )
                    inspeccion.registrar_reporte(reporte)

                elif muestra.getter_estado() != "CONFORME":
                    raise ValueError(
                        "Una inspección finalizada debe tener una muestra cerrada."
                    )

                profesional.restaurar_inspeccion_finalizada(
                    inspeccion
                )

        # 12. Restaurar estados de los lotes
        for lote in empresa.getter_lotes():

            lote.restaurar_estado(
                estados_lotes[lote.getter_id()]
            )

    
    def guardar_estado_total(self, empresa):
        profesionales = empresa.getter_profesionales()
        equipos = empresa.getter_equipos()
        lotes = empresa.getter_lotes()

        # 1. Administradores
        self._guardar(
            "administradores.csv",
            ["id", "nombre"],
            list(map(
                lambda a: {
                    "id": a.getter_id(),
                    "nombre": a.getter_nombre()
                },
                empresa.getter_administradores()
            ))
        )

        # 2. Profesionales
        self._guardar(
            "profesionales.csv",
            ["id", "nombre"],
            list(map(
                lambda p: {
                    "id": p.getter_id(),
                    "nombre": p.getter_nombre()
                },
                profesionales
            ))
        )

        # 3. Certificaciones
        certificaciones = [
            {
                "profesional_id": p.getter_id(),
                "nombre": c.getter_nombre(),
                "fecha_inicio": c.getter_fecha_inicio().isoformat(),
                "fecha_vencimiento": c.getter_fecha_vencimiento().isoformat()
            }
            for p in profesionales
            for c in p.getter_certificaciones()
        ]

        self._guardar(
            "certificaciones.csv",
            ["profesional_id", "nombre", "fecha_inicio", "fecha_vencimiento"],
            certificaciones
        )

        # 4. Equipos
        self._guardar(
            "equipos.csv",
            ["id", "categoria"],
            list(map(
                lambda e: {
                    "id": e.getter_id(),
                    "categoria": e.getter_categoria()
                },
                equipos
            ))
        )

        # 5. Calibraciones
        calibraciones = [
            {
                "equipo_id": e.getter_id(),
                "fecha": fecha.isoformat()
            }
            for e in equipos
            for fecha in e.getter_calibraciones()
        ]

        self._guardar(
            "calibraciones.csv",
            ["equipo_id", "fecha"],
            calibraciones
        )

        # 6. Procedimientos
        procedimientos = []

        for p in empresa.getter_procedimientos():
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
                fila.update({
                    "tipo": "dimensional",
                    "valor_esperado": p.getter_valor_esperado(),
                    "tolerancia": p.getter_tolerancia(),
                    "desvio": p.getter_desvio(),
                    "rangos_gravedad": json.dumps(
                        p.getter_rangos_gravedad(),
                        ensure_ascii=False
                    )
                })

            elif isinstance(p, ProcedimientoVisual):
                fila.update({
                    "tipo": "visual",
                    "probabilidad": p.getter_probabilidad(),
                    "zonas_posibles": json.dumps(
                        p.getter_zonas_posibles(),
                        ensure_ascii=False
                    ),
                    "descripciones": json.dumps(
                        p.getter_descripciones(),
                        ensure_ascii=False
                    )
                })

            procedimientos.append(fila)

        self._guardar(
            "procedimientos.csv",
            [
                "id", "tipo", "nombre", "categoria_equipo",
                "certificaciones_requeridas", "limite_gravedad",
                "valor_esperado", "tolerancia", "desvio",
                "rangos_gravedad", "probabilidad",
                "zonas_posibles", "descripciones"
            ],
            procedimientos
        )

        # 7. Obtener todas las muestras de los lotes
        muestras = [
            m
            for lote in lotes
            for m in lote.getter_muestras()
        ]

        # Guardar reportes sin sobrescribir los existentes
        for muestra in muestras:
            inspeccion = muestra.getter_inspeccion()

            if inspeccion is not None:
                reporte = inspeccion.getter_reporte()

                if reporte is not None:
                    GestorArchivos.guardar_reporte(
                        reporte.getter_id(),
                        reporte.crear_resumen()
                    )

        # 8. Lotes
        self._guardar(
            "lotes.csv",
            ["id", "cantidad_fabricada", "estado"],
            list(map(
                lambda lote: {
                    "id": lote.getter_id(),
                    "cantidad_fabricada": lote.getter_cantidad_fabricada(),
                    "estado": lote.getter_estado()
                },
                lotes
            ))
        )

        # 9. Muestras
        self._guardar(
            "muestras.csv",
            ["id", "lote_id", "unidades", "estado"],
            list(map(
                lambda m: {
                    "id": m.getter_id(),
                    "lote_id": m.getter_lote().getter_id(),
                    "unidades": m.getter_unidadesrepresentadas(),
                    "estado": m.getter_estado()
                },
                muestras
            ))
        )

        # 10. Defectos
        defectos = [
            {
                "muestra_id": m.getter_id(),
                "tipo": d.getter_tipo(),
                "gravedad": d.getter_gravedad(),
                "descripcion": d.getter_descripcion()
            }
            for m in muestras
            for d in m.getter_defectos()
        ]

        self._guardar(
            "defectos.csv",
            ["muestra_id", "tipo", "gravedad", "descripcion"],
            defectos
        )

        # 11. Inspecciones finalizadas en orden cronológico por profesional
        finalizadas = [
            i
            for p in profesionales
            for i in reversed(p.getter_historial())
        ]

        # Inspecciones pendientes en orden FIFO por profesional
        pendientes = [
            i
            for p in profesionales
            for i in p.getter_inspecciones_pendientes()
        ]


        
        estados_inspecciones = {
            i.getter_id(): (
                "REPORTE_PENDIENTE"
                if i.getter_muestra().getter_estado() == "NO_CONFORME"
                else "PENDIENTE"
            )
            for i in pendientes
        }

        estados_inspecciones.update({
            i.getter_id(): "FINALIZADA"
            for i in finalizadas
        })

        
        # Convertir todas las inspecciones en filas CSV
        filas_inspecciones = list(map(
            lambda i: {
                "id": i.getter_id(),
                "muestra_id": i.getter_muestra().getter_id(),
                "fecha": i.getter_fecha().isoformat(),
                "profesional_id": i.getter_profesional().getter_id(),
                "equipo_id": i.getter_equipo().getter_id(),
                "procedimiento_id": i.getter_procedimiento().getter_id(),
                "estado_inspeccion": estados_inspecciones[i.getter_id()]
            },
            pendientes + finalizadas
        ))

        
        self._guardar(
            "inspecciones.csv",
            [
                "id", "muestra_id", "fecha",
                "profesional_id", "equipo_id",
                "procedimiento_id", "estado_inspeccion"
            ],
            filas_inspecciones
        )
