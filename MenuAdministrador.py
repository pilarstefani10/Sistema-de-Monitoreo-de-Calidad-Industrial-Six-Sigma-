class MenuAdministrador:

    def __init__(self, empresa, administrador):
        self.__empresa = empresa
        self.__administrador = administrador

    def iniciar(self):
        opcion = ""

        while opcion != "0":
            print("\n\n==========================================")
            print("          MENÚ ADMINISTRADOR")
            print("==========================================\n")
            print("   1. Ver lotes")
            print("   2. Crear lote")
            print("   3. Crear muestra y asignar inspección")
            print("   4. Evaluar lote")
            print("   0. Salir\n")

            opcion = input("Opción: ")

            try:
                if opcion == "1":
                    self.ver_lotes()
                elif opcion == "2":
                    self.crear_lote()
                elif opcion == "3":
                    self.crear_muestra()
                elif opcion == "4":
                    self.evaluar_lote()
                elif opcion == "0":
                    print("\nSesión finalizada.\n")
                else:
                    print("\nOpción incorrecta.")

            except ValueError as error:
                print("\nError:", error)

            if opcion != "0":
                input("\nPresione ENTER para volver al menú principal...")

    def ver_lotes(self):
        print("\n---------- LOTES ----------\n")
        for lote in self.__empresa.getter_lotes():
            print(lote.getter_id(), "- Estado:", lote.getter_estado(),
                  "- Muestras:", len(lote.getter_muestras()))

    def crear_lote(self):
        cantidad = self.pedir_entero("\nCantidad fabricada: ")
        lote = self.__administrador.crear_lote(cantidad)
        print("\nLote creado:", lote.getter_id())

    def crear_muestra(self):
        self.ver_lotes()

        print("\n---------- PROFESIONALES ----------\n")
        for profesional in self.__empresa.getter_profesionales():
            print(profesional.getter_id(), "-", profesional.getter_nombre())

        print("\n---------- EQUIPOS ----------\n")
        for equipo in self.__empresa.getter_equipos():
            print(equipo.getter_id(), "-", equipo.getter_categoria(),
                  "- Última calibración:", equipo.getter_ultima_calibracion())

        print("\n---------- PROCEDIMIENTOS ----------\n")
        for procedimiento in self.__empresa.getter_procedimientos():
            print(procedimiento.getter_id(), "-", procedimiento.getter_nombre())

        id_lote = input("\nID del lote: ")
        unidades = self.pedir_entero("Unidades de la muestra: ")
        id_profesional = input("ID del profesional: ")
        id_equipo = input("ID del equipo: ")
        id_procedimiento = input("ID del procedimiento: ")

        muestra = self.__administrador.crear_muestra(
            id_lote, unidades, id_profesional, id_equipo, id_procedimiento)

        print("\nMuestra", muestra.getter_id(), "creada y asignada a", id_profesional)

    def evaluar_lote(self):
        self.ver_lotes()
        id_lote = input("\nID del lote a evaluar: ")
        estado = self.__administrador.evaluar_lote(id_lote)
        print("\nEl lote", id_lote, "quedó", estado)

    @staticmethod
    def pedir_entero(mensaje):
        texto = input(mensaje)
        if not texto.isdigit():
            raise ValueError("Debe ingresar un número entero positivo.")
        return int(texto)