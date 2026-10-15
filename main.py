from datetime import date
from Empresa import Empresa
from Administrador import Administrador
from Profesional import Profesional
from Equipo import Equipo
from MenuAdministrador import MenuAdministrador
from MenuProfesional import MenuProfesional


# ---------- Datos iniciales ----------

empresa = Empresa("QuantumTech Precision")
admin = Administrador("Carla Diaz", empresa)

ana = Profesional("Ana Perez")
luis = Profesional("Luis Gomez")
admin.registrar_profesional(ana)
admin.registrar_profesional(luis)

ana.agregar_certificacion("Control de leche", date(2026, 1, 1), date(2027, 1, 1))
luis.agregar_certificacion("Control de leche", date(2026, 1, 1), date(2027, 1, 1))

admin.registrar_equipo(Equipo("volumen", date(2026, 8, 1)))
admin.registrar_equipo(Equipo("volumen", date(2025, 1, 1)))

admin.crear_procedimiento(
    "dimensional",
    nombre="Control de volumen",
    categoria_equipo_requerida="volumen",
    certificacion_requerida="Control de leche",
    limite_gravedad=3,
    valor_esperado=1000.0,
    tolerancia=5.0,
    desvio=3.0,
    rangos_gravedad={"leve": 7, "moderado": 9, "serio": 11, "severo": 13, "crítico": 15}
)

admin.crear_procedimiento(
    "visual",
    nombre="Control de envase",
    categoria_equipo_requerida="volumen",
    certificacion_requerida="Control de leche",
    probabilidad=0.1,
    zonas_posibles=["tapa", "base", "etiqueta"],
    descripciones=["Fisura", "Abolladura", "Mancha"]
)

admin.crear_lote(100)
admin.crear_muestra("L1", 5, "P1", "E1", "PR1")
admin.crear_muestra("L1", 5, "P1", "E1", "PR1")
admin.crear_muestra("L1", 5, "P2", "E1", "PR2")


# ---------- Ingreso ----------

while True:
    print("\n==========================================")
    print("       CONTROL DE CALIDAD DE LECHE")
    print("==========================================\n")

    nombre = input("Nombre (ENTER para salir del sistema): ")
    if nombre == "":
        break

    ID = input("ID: ")

    try:
        empleado = empresa.buscar_empleado(nombre, ID)

        print("\nBienvenido/a", empleado.getter_nombre())

        if isinstance(empleado, Administrador):
            MenuAdministrador(empresa, empleado).iniciar()
        else:
            MenuProfesional(empresa, empleado).iniciar()

    except ValueError as error:
        print("\nError:", error)

print("\nSistema cerrado.\n")