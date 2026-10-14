from datetime import date, datetime

class MenuProfesional:

    def __init__(self, empresa, profesional):
        self.__empresa = empresa
        self.__profesional = profesional

    def iniciar(self):
        opcion = ""

        while opcion != "0":
            print("\n\n==========================================")
            print("           MENÚ PROFESIONAL")
            print("==========================================\n")
            print("   1. Ver inspecciones pendientes")
            print("   2. Ejecutar siguiente inspección")
            print("   3. Agregar certificación")
            print("   4. Calibrar equipo")
            print("   0. Salir\n")

            opcion = input("Opción: ")

            try:
                if opcion == "1":
                    self.ver_pendientes()
                elif opcion == "2":
                    self.ejecutar_siguiente()
                elif opcion == "3":
                    self.agregar_certificacion()
                elif opcion == "4":
                    self.calibrar_equipo()
                elif opcion == "0":
                    print("\nSesión finalizada.\n")
                else:
                    print("\nOpción incorrecta.")

            except ValueError as error:
                print("\nError:", error)

            if opcion != "0":
                input("\nPresione ENTER para volver al menú principal...")

    def ver_pendientes(self):
        print("\n---------- INSPECCIONES PENDIENTES ----------\n")
        pendientes = self.__profesional.getter_inspecciones_pendientes()

        if len(pendientes) == 0:
            print("No tiene inspecciones pendientes.")

        for inspeccion in pendientes:
            print(inspeccion.getter_id(), "- Muestra:", inspeccion.getter_muestra().getter_id(),
                  "- Procedimiento:", inspeccion.getter_procedimiento().getter_nombre())

    def ejecutar_siguiente(self):
        inspeccion = self.__profesional.ejecutar_siguiente_inspeccion()
        muestra = inspeccion.getter_muestra()

        print("\nResultado de la muestra", muestra.getter_id() + ":", muestra.getter_estado())

        defectos = muestra.getter_defectos()
        if len(defectos) == 0:
            print("\nNo se encontraron defectos.")
        else:
            print("\nDefectos encontrados:\n")
            for defecto in defectos:
                print("   -", defecto)

        if inspeccion.getter_reporte() is not None:
            print(inspeccion.getter_reporte().crear_resumen())

    def agregar_certificacion(self):
        nombre = input("\nNombre de la certificación: ")
        inicio = self.pedir_fecha("Fecha de inicio:")
        vencimiento = self.pedir_fecha("Fecha de vencimiento:")

        self.__profesional.agregar_certificacion(nombre, inicio, vencimiento)
        print("\nCertificación agregada.")

    def calibrar_equipo(self):
        print("\n---------- EQUIPOS ----------\n")
        for equipo in self.__empresa.getter_equipos():
            print(equipo.getter_id(), "-", equipo.getter_categoria(),
                  "- Última calibración:", equipo.getter_ultima_calibracion())

        id_equipo = input("\nID del equipo a calibrar: ")
        equipo = self.__empresa.buscar_equipo(id_equipo)

        self.__profesional.calibrar_equipo(equipo, date.today())
        print("\nEquipo", id_equipo, "calibrado.")

    @staticmethod
    def pedir_fecha(mensaje):
        print(mensaje)
        dia = int(input("  Día: "))
        mes = int(input("  Mes: "))
        anio = int(input("  Año: "))
        return date(anio, mes, dia)