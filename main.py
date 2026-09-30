from datetime import date
from Lote import Lote
from Profesional import Profesional
from Defecto import Defecto
from Certificacion import Certificacion
from Equipo import Equipo
from ProcedimientoDimensional import ProcedimientoDimensional
from ProcedimientoVisual import ProcedimientoVisual
from Reporte import Reporte
from Muestra import Muestra

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

procedimiento = ProcedimientoDimensional(
    nombre="Control de volumen",
    categoria_equipo_requerida="volumen",
    certificacion_requerida="Control de leche",
    limite_gravedad=3,
    valor_esperado=1000.0,   
    tolerancia=5.0,          
    desvio=3.0,              
    rangos_gravedad={"leve": 7, "moderado": 9, "serio": 11, "severo": 13, "crítico": 15}
)

procedimiento_visual = ProcedimientoVisual(
    nombre="Control de envase",
    categoria_equipo_requerida="volumen",
    certificacion_requerida="Control de leche",
    probabilidad=0.1,
    zonas_posibles=["tapa", "base", "etiqueta"],
    descripciones=["Fisura", "Abolladura", "Mancha"]
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
    procedimiento_visual
)



#INGRESO


print("\n==========================================")
print("       CONTROL DE CALIDAD DE LECHE")
print("==========================================\n")
 
nombre = input("Nombre: ")
ID = input("ID: ")
 
profesional_actual = Profesional.buscar_profesional(nombre, ID)
 
if profesional_actual is None:
 
    print("\nProfesional incorrecto.\n")
 
else:
 
    print("\nBienvenido/a", profesional_actual.name)
    opcion = ""
 
    while opcion != "0":
 
        print("\n\n==========================================")
        print("              MENÚ PRINCIPAL")
        print("==========================================\n")
        print("   1. Ver mis inspecciones")
        print("   0. Salir\n")
 
        opcion = input("Opción: ")
 
 
        if opcion == "1":
 
            inspecciones = profesional_actual.obtener_inspecciones(
                lote.getter_muestras()
            )
 
            print("\n\n---------- MIS INSPECCIONES ----------\n")
 
            if len(inspecciones) == 0:
                print("No tiene inspecciones.")
 
            else:
 
                pendientes = []
 
                for inspeccion in inspecciones:
                    print("Inspección:", inspeccion.ID)
                    print("Muestra:", inspeccion.getter_muestra().ID)
                    print("Procedimiento:", inspeccion.getter_procedimiento().getter_nombre())
                    print("Estado:", inspeccion.getter_muestra().getter_estado())
                    print()
 
                    if inspeccion.getter_muestra().getter_estado() == "EN_INSPECCION":
                        pendientes.append(inspeccion)
 
                if len(pendientes) == 0:
                    print("No tiene inspecciones pendientes para ejecutar.")
 
                else:
 
                    respuesta = input("¿Desea ejecutar alguna inspección? (si/no): ")
 
                    if respuesta == "si":
 
                        id_elegido = input("\nID de la inspección a ejecutar: ")
 
                        elegida = None
                        for inspeccion in pendientes:
                            if inspeccion.ID == id_elegido:
                                elegida = inspeccion
 
                        if elegida is None:
                            print("\nNo existe una inspección pendiente con ese ID.")
 
                        else:
                            try:
                                elegida.ejecutar()
                                muestra = elegida.getter_muestra()
 
                                print("\nResultado de la muestra", muestra.ID + ":", muestra.getter_estado())
 
                                defectos = muestra.getter_defectos()
                                if len(defectos) == 0:
                                    print("\nNo se encontraron defectos.")
                                else:
                                    print("\nDefectos encontrados:\n")
                                    for defecto in defectos:
                                        print("   -", defecto)
 
                            except ValueError as error:
                                print("\nNo se pudo ejecutar la inspección:", error)
 
            input("\nPresione ENTER para volver al menú principal...")
 
 
        elif opcion == "0":
 
            print("\nSesión finalizada.\n")
 
        else:
 
            print("\nOpción incorrecta.")
            input("\nPresione ENTER para volver al menú principal...")
 