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

# Crear datos iniciales

ana = Profesional("Ana Perez")
luis = Profesional("Luis Gomez")

certificacion = Certificacion(
    "Control de leche",
    date(2026, 1, 1),
    date(2027, 1, 1)
)

ana.agregar_certificacion(certificacion)
luis.agregar_certificacion(certificacion)

equipo = Equipo(
    "volumen",
    date(2026, 8, 1)
)

procedimiento = Procedimiento(
    "Control de volumen",
    "volumen",
    "Control de leche",
    3
)

lote = Lote(100)

muestra1 = lote.crear_muestra(
    date.today(),
    ana,
    equipo,
    procedimiento
)

muestra2 = lote.crear_muestra(
    date.today(),
    ana,
    equipo,
    procedimiento
)

muestra3 = lote.crear_muestra(
    date.today(),
    luis,
    equipo,
    procedimiento
)



# INGRESO

print("===== CONTROL DE CALIDAD DE LECHE =====")

nombre = input("Nombre: ")
ID = input("ID: ")

profesional_actual = Profesional.buscar_profesional(nombre, ID)
if profesional_actual is None:

    print("Profesional incorrecto.")

else:

    print("\nBienvenido/a", profesional_actual.name)
    opcion = ""

    while opcion != "0":

        print("\n===== MENÚ PRINCIPAL =====")
        print("1. Ver mis inspecciones")
        print("0. Salir")


        opcion = input("Opción: ")


        if opcion == "1":

            inspecciones = profesional_actual.obtener_inspecciones(
                lote.muestras
            )
            print("\n--- MIS INSPECCIONES ---")

            if len(inspecciones) == 0:
                print("No tiene inspecciones.")

            else:

                for inspeccion in inspecciones:
                    print(
                        inspeccion.ID,
                        "- Muestra:",
                        inspeccion.muestra.ID,
                        "- Procedimiento:",
                        inspeccion.procedimiento.nombre
                    )


        elif opcion == "0":

            print("Sesión finalizada.")


        else:

            print("Opción incorrecta.")