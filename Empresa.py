from Excepciones import DatosInvalidosError
from persistencia import Persistencia
from Arbol import Arbol
class Empresa:
#La idea es que haya una única empresa o instancia que funcionará como un repertorio universal donde se añaden todos los profesionales, lotes, procedimientos, equipos y certificaciones
    def __init__(self, nombre):
        if not nombre:
            raise DatosInvalidosError("El nombre no puede estar vacío")

        self.__nombre = nombre
        self.__lotes = {}#Combiene más en diccionarios separados porque sino sería un diccionarios con listas
        self.__profesionales = {}#Y perdería sentido
        self.__equipos = {}
        self.__procedimientos = {}
        self.__administradores = {}
        self.__arbol_lotes=Arbol()
        self.__persistencia = Persistencia()

    def registrar_lote(self, lote):
        if lote.getter_id() in self.__lotes:
            raise DatosInvalidosError("ID de lote duplicado")

        self.__arbol_lotes.insertar(lote)
        self.__lotes[lote.getter_id()] = lote

    def registrar_profesional(self, profesional):
        if profesional.getter_id() in self.__profesionales:
            raise DatosInvalidosError("ID de profesional duplicado")

        self.__profesionales[profesional.getter_id()] = profesional
        

    def registrar_administrador(self, administrador):
        if administrador.getter_id() in self.__administradores:
            raise DatosInvalidosError("ID de administrador duplicado")

        self.__administradores[administrador.getter_id()] = administrador

    def registrar_equipo(self, equipo):
        if equipo.getter_id() in self.__equipos:
            raise DatosInvalidosError("ID de equipo duplicado")

        self.__equipos[equipo.getter_id()] = equipo

    def registrar_procedimiento(self, procedimiento):
        if procedimiento.getter_id() in self.__procedimientos:
            raise DatosInvalidosError("ID de procedimiento duplicado")

        self.__procedimientos[procedimiento.getter_id()] = procedimiento

    @staticmethod
    def buscar(diccionario, ID, tipo):
        if ID not in diccionario:
            raise DatosInvalidosError("No existe un " + tipo + " con el ID " + str(ID) + ".")
        return diccionario[ID]

    def buscar_lote(self, ID):
        return Empresa.buscar(self.__lotes, ID, "lote")

    def buscar_lote_arbol(self, ID):
        if not isinstance(ID, str) or not ID.startswith("L") or not ID[1:].isdigit():
            raise DatosInvalidosError("ID de lote inválido")

        numero = int(ID[1:])
        lote = self.__arbol_lotes.buscar(self.__arbol_lotes.raiz, numero)

        if lote is None or lote.getter_id() != ID:
            raise DatosInvalidosError("No existe un lote con ese ID")

        return lote

    def obtener_lotes_ordenados(self):
        return self.__arbol_lotes.inorden(self.__arbol_lotes.raiz)

    def buscar_profesional(self, ID):
        return Empresa.buscar(self.__profesionales, ID, "profesional")

    def buscar_equipo(self, ID):
        return Empresa.buscar(self.__equipos, ID, "equipo")

    def buscar_procedimiento(self, ID):
        return Empresa.buscar(self.__procedimientos, ID, "procedimiento")

    def getter_equipos(self):
        return list(self.__equipos.values())

    def getter_lotes(self):
        return list(self.__lotes.values())

    def getter_profesionales(self):
        return list(self.__profesionales.values())

    def getter_procedimientos(self):
        return list(self.__procedimientos.values())

    def buscar_empleado(self, nombre, ID):
        if ID in self.__profesionales:
            empleado = self.__profesionales[ID]
        elif ID in self.__administradores:
            empleado = self.__administradores[ID]
        else:
            raise DatosInvalidosError("No existe un empleado con el ID " + str(ID) + ".")

        if empleado.getter_nombre() != nombre:
            raise DatosInvalidosError("El nombre no coincide con el ID ingresado.")

        return empleado

    def getter_administradores(self):
        return list(self.__administradores.values())

    
    def reconstruir_arbol_lotes(self):
        self.__arbol_lotes.construir_balanceado(
            self.__lotes.values()
        )

    def cargar_estado_total(self):
        self.__persistencia.cargar_estado_total(self)

    def guardar_estado_total(self):
        self.__persistencia.guardar_estado_total(self)



   

        