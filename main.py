from datetime import date
from Lote import Lote
from Profesional import Profesional
from Defecto import Defecto
from Certificacion import Certificacion
from Equipo import Equipo
from Procedimiento import Procedimiento
from Reporte import Reporte

# lote = Lote(100)
# muestra = lote.crear_muestra()

# defecto1 = Defecto("Tipo A", 4, "Descripción del defecto A")
# defecto2 = Defecto("Tipo A", 3,"Descripción del defecto A")
# muestra.registrar_defecto(defecto2)
# muestra.registrar_defecto(defecto1)


# print("Cantidad de muestras en el lote:", len(lote.muestras))
# print("La muestra conoce a su lote:", muestra.lote is lote)
# print("Defectos registrados en la muestra:")
# for defecto in muestra.defectos:
#     print(defecto)


# ana = Profesional("Ana Perez")
# luis = Profesional("Luis Gomez")

# certificacion = Certificacion("Certificacion A", date(2026, 1, 1), date(2027, 1, 1))
# ana.agregar_certificacion(certificacion)

# equipo = Equipo("metal", date(2026, 8, 1))
# procedimiento = Procedimiento(
# 	"Control visual",
# 	"metal",
# 	"Certificacion A",
# 	3
# )

# inspeccion = muestra.iniciar_inspeccion(date.today(),ana,equipo,procedimiento)

# print(inspeccion)

# print(ana)



#reporte = Reporte(
#    "1",
#    date.today(),
#    muestra,
#    lote,
#    ana)

# Mostrar resumen
#print(reporte.crear_resumen())

from datetime import date

from Lote import Lote
from Profesional import Profesional
from Certificacion import Certificacion
from Equipo import Equipo
from Procedimiento import Procedimiento


# =========================================
# CREACIÓN DE DATOS
# =========================================

# Creamos el lote de leche
lote = Lote(100)

# Creamos dos muestras
muestra1 = lote.crear_muestra()
muestra2 = lote.crear_muestra()


# Creamos profesionales
ana = Profesional("Ana Perez")
luis = Profesional("Luis Gomez")


# Creamos certificación
certificacion = Certificacion(
    "Control de leche",
    date(2026, 1, 1),
    date(2027, 1, 1)
)

ana.agregar_certificacion(certificacion)
luis.agregar_certificacion(certificacion)


# Creamos equipo
equipo = Equipo(
    "volumen",
    date(2026, 8, 1)
)


# Creamos procedimiento
procedimiento = Procedimiento(
    "Control de volumen",
    "volumen",
    "Control de leche",
    3
)


# =========================================
# ASIGNACIÓN DE INSPECCIONES
# =========================================

inspecciones_asignadas = {
    ana.ID: [
        [muestra1, equipo, procedimiento]
    ],

    luis.ID: [
        [muestra2, equipo, procedimiento]
    ]
}


# Lista de profesionales existentes
profesionales = [ana, luis]


# =========================================
# INGRESO AL SISTEMA
# =========================================

print("===================================")
print(" SISTEMA DE CONTROL DE CALIDAD")
print(" Producto: Leche")
print("===================================")

nombre = input("Nombre: ")
id_ingresado = input("ID: ")


profesional_actual = None


for profesional in profesionales:

    if profesional.name == nombre and profesional.ID == id_ingresado:

        profesional_actual = profesional


# =========================================
# VALIDACIÓN DEL INGRESO
# =========================================

if profesional_actual is None:

    print("Nombre o ID incorrecto.")


else:

    print()
    print("Bienvenido/a", profesional_actual.name)


    opcion = ""

    while opcion != "0":

        print()
        print("========= MENÚ =========")
        print("1. Ver inspecciones pendientes")
        print("2. Iniciar inspección")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")


        # =================================
        # VER INSPECCIONES PENDIENTES
        # =================================

        if opcion == "1":

            print()
            print("--- INSPECCIONES PENDIENTES ---")

            asignaciones = inspecciones_asignadas[profesional_actual.ID]

            for i in range(len(asignaciones)):

                muestra = asignaciones[i][0]
                procedimiento_asignado = asignaciones[i][2]

                if muestra.estado == "PENDIENTE":

                    print(
                        i + 1,
                        "- Muestra:",
                        muestra.ID,
                        "- Procedimiento:",
                        procedimiento_asignado.nombre
                    )


        # =================================
        # INICIAR INSPECCIÓN
        # =================================

        elif opcion == "2":

            asignaciones = inspecciones_asignadas[profesional_actual.ID]

            print()
            print("--- SELECCIONE UNA INSPECCIÓN ---")

            for i in range(len(asignaciones)):

                muestra = asignaciones[i][0]

                if muestra.estado == "PENDIENTE":

                    print(
                        i + 1,
                        "-",
                        muestra.ID
                    )


            numero = int(input("Número de inspección: "))

            asignacion = asignaciones[numero - 1]

            muestra = asignacion[0]
            equipo_asignado = asignacion[1]
            procedimiento_asignado = asignacion[2]


            try:

                inspeccion = muestra.iniciar_inspeccion(
                    date(2026, 9, 24),
                    profesional_actual,
                    equipo_asignado,
                    procedimiento_asignado
                )

                print()
                print("Inspección iniciada correctamente.")
                print("Muestra:", muestra.ID)
                print("Estado:", muestra.estado)
                print("Procedimiento:", procedimiento_asignado.nombre)


            except ValueError as error:

                print()
                print("No se pudo iniciar la inspección.")
                print(error)


        elif opcion == "0":

            print("Sesión finalizada.")


        else:

            print("Opción incorrecta.")
