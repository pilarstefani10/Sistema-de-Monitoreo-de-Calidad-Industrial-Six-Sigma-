from datetime import date
from Empresa import Empresa
from Administrador import Administrador
from MenuAdministrador import MenuAdministrador
from MenuProfesional import MenuProfesional
from Excepciones import QuantumTechError


# ---------- Datos iniciales ----------
empresa = Empresa("QuantumTech Precision")
empresa.cargar_estado_total()

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

    except (QuantumTechError, ValueError) as error:
        print("\nError:", error)

empresa.guardar_estado_total()
print("\nDatos guardados correctamente.")
print("\nSistema cerrado.\n")