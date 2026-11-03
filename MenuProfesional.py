from datetime import date, datetime
from Excepciones import QuantumTechError

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
            print("   2. Ver última inspección realizada")
            print("   3. Ejecutar siguiente inspección")
            print("   4. Ver historial de inspecciones")
            print("   5. Agregar certificación")
            print("   6. Calibrar equipo")
            print("   7. Dar de baja una calibración")
            print("   8. Ver historial de calibraciones de un equipo")
            print("   9. Ver mis certificaciones")
            print("   0. Salir\n")

            opcion = input("Opción: ")

            try:
                if opcion == "1":
                    self.ver_pendientes()
                elif opcion == "2":
                    self.ver_ultima_inspeccion()
                elif opcion == "3":
                    self.ejecutar_siguiente()
                elif opcion == "4":
                    self.ver_historial()
                elif opcion == "5":
                    self.agregar_certificacion()
                elif opcion == "6":
                    self.calibrar_equipo()
                elif opcion == "7":
                    self.eliminar_calibracion()
                elif opcion == "8":
                    self.ver_calibraciones()
                elif opcion == "9":
                    self.ver_certificaciones()                    
                elif opcion == "0":
                    print("\nSesión finalizada.\n")
                else:
                    print("\nOpción incorrecta.")

            except (QuantumTechError, ValueError) as error:
                print("\nError:", error)

            if opcion != "0":
                input("\nPresione ENTER para volver al menú principal...")

    def ver_pendientes(self):
        print("\n---------- INSPECCIONES PENDIENTES ----------\n")
        pendientes = self.__profesional.getter_inspecciones_pendientes()

        if len(pendientes) == 0:
            print("No tiene inspecciones pendientes.")

        print("\n".join(map(
            lambda inspeccion: inspeccion.getter_id()
            + " - Muestra: " + inspeccion.getter_muestra().getter_id()
            + " - Procedimiento: " + inspeccion.getter_procedimiento().getter_nombre(),
            pendientes)))

    def ejecutar_siguiente(self):
        inspeccion = self.__profesional.ejecutar_siguiente_inspeccion()
        muestra = inspeccion.getter_muestra()

        print("\nResultado de la muestra", muestra.getter_id() + ":", muestra.getter_estado())

        defectos = muestra.getter_defectos()
        if len(defectos) == 0:
            print("\nNo se encontraron defectos.")
        else:
            print("\nDefectos encontrados:\n")
            print("\n".join(map(
                lambda defecto: "   - " + str(defecto),
                defectos)))
        if inspeccion.getter_reporte() is not None:
            reporte = inspeccion.getter_reporte()
            print(reporte.crear_resumen()) 
            print(reporte.impacto_preliminar())

    def agregar_certificacion(self):
        nombre = input("\nNombre de la certificación: ")
        inicio = self.pedir_fecha("Fecha de inicio:")
        vencimiento = self.pedir_fecha("Fecha de vencimiento:")

        self.__profesional.agregar_certificacion(nombre, inicio, vencimiento)
        print("\nCertificación agregada.")

    def ver_equipos(self):
        print("\n---------- EQUIPOS ----------\n")
        print("\n".join(map(lambda equipo: equipo.getter_id() + " - " + equipo.getter_categoria() + " - Última calibración: " + str(equipo.getter_ultima_calibracion()), self.__empresa.getter_equipos())))

    def calibrar_equipo(self):
        self.ver_equipos()
        equipo = self.__empresa.buscar_equipo(input("\nID del equipo a calibrar: "))

        print("\n   1. Calibrar ahora")
        print("   2. Registrar una calibración anterior")
        tipo = input("\nOpción: ")

        if tipo == "1":
            fecha = date.today()
        elif tipo == "2":
            fecha = self.pedir_fecha("Fecha de la calibración:")
        else:
            raise ValueError("Opción incorrecta.")

        self.__profesional.calibrar_equipo(equipo, fecha)
        print("\nEquipo", equipo.getter_id(), "calibrado el", fecha)

    def ver_ultima_inspeccion(self):
        inspeccion = self.__profesional.getter_ultima_inspeccion()

        if inspeccion is None:
            print("\nTodavía no realizó inspecciones.")
            return

        print("\n---------- ÚLTIMA INSPECCIÓN ----------\n")
        print(inspeccion)
        print("Resultado:", inspeccion.getter_muestra().getter_estado())

        if inspeccion.getter_reporte() is not None:
            print(inspeccion.getter_reporte().crear_resumen())
            print(inspeccion.getter_reporte().impacto_preliminar())

    def ver_historial(self):
        historial = self.__profesional.getter_historial()

        if len(historial) == 0:
            print("\nTodavía no realizó inspecciones.")
            return

        print("\n---------- HISTORIAL (de la más reciente a la más antigua) ----------\n")
        print("\n".join(map(lambda inspeccion: inspeccion.getter_id() + " - Muestra: " + inspeccion.getter_muestra().getter_id() + " - " + inspeccion.getter_muestra().getter_estado(), historial)))

    def ver_calibraciones(self):
        self.ver_equipos()
        equipo = self.__empresa.buscar_equipo(input("\nID del equipo: "))
        calibraciones = equipo.getter_calibraciones()

        if len(calibraciones) == 0:
            print("\nEl equipo no tiene calibraciones.")
            return

        print("\n---------- CALIBRACIONES DE", equipo.getter_id(), "(de la más antigua a la más reciente) ----------\n")
        print("\n".join(map(str, calibraciones)))
        print("\n¿Apto hoy?:", "Sí" if equipo.calibracion_vigente(date.today()) else "No")

    def eliminar_calibracion(self):
        self.ver_equipos()
        equipo = self.__empresa.buscar_equipo(input("\nID del equipo: "))
        print("\nCalibraciones:", ", ".join(map(str, equipo.getter_calibraciones())))
        fecha = self.pedir_fecha("Fecha de la calibración a dar de baja:")

        self.__profesional.eliminar_calibracion(equipo, fecha)
        print("\nCalibración del", fecha, "dada de baja.")

    def ver_certificaciones(self):
        certificaciones = self.__profesional.getter_certificaciones()

        if len(certificaciones) == 0:
            print("\nNo tiene certificaciones cargadas.")
            return

        print("\n---------- MIS CERTIFICACIONES ----------\n")
        print("\n".join(map(lambda cert: cert.getter_nombre() + " - Desde: " + str(cert.getter_fecha_inicio()) + " - Hasta: " + str(cert.getter_fecha_vencimiento()) + " - " + ("Vigente" if cert.esta_vigente(date.today()) else "Vencida"), certificaciones)))
    
    @staticmethod
    def pedir_fecha(mensaje):
        print(mensaje)
        dia = int(input("  Día: "))
        mes = int(input("  Mes: "))
        anio = int(input("  Año: "))
        return date(anio, mes, dia)