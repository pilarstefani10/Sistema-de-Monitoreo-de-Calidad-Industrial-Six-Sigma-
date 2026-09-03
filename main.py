from datetime import date
from Lote import Lote
from Profesional import Profesional
from Defecto import Defecto
from Certificacion import Certificacion
from Equipo import Equipo
from Procedimiento import Procedimiento
from Reporte import Reporte

lote = Lote(100)
muestra = lote.crear_muestra()

defecto1 = Defecto("Tipo A", 4, "Descripción del defecto A")
defecto2 = Defecto("Tipo A", 3,"Descripción del defecto A")
muestra.registrar_defecto(defecto2)
muestra.registrar_defecto(defecto1)


print("Cantidad de muestras en el lote:", len(lote.muestras))
print("La muestra conoce a su lote:", muestra.lote is lote)
print("Defectos registrados en la muestra:")
for defecto in muestra.defectos:
    print(defecto)


ana = Profesional("Ana Perez")
luis = Profesional("Luis Gomez")

certificacion = Certificacion("Certificacion A", date(2026, 1, 1), date(2027, 1, 1))
ana.agregar_certificacion(certificacion)

equipo = Equipo("10", "metal", date(2026, 8, 1))
procedimiento = Procedimiento(
	"Control visual",
	"metal",
	"Certificacion A",
	3
)

inspeccion = muestra.iniciar_inspeccion(date.today(),ana,equipo,procedimiento)

print(inspeccion)

print(ana)



#reporte = Reporte(
#    "1",
#    date.today(),
#    muestra,
#    lote,
#    ana)

# Mostrar resumen
#print(reporte.crear_resumen())