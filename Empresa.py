class Empresa:
#La idea es que haya una única empresa o instancia que funcionará como un repertorio universal donde se añaden todos los profesionales, lotes, procedimientos, equipos y certificaciones
    def __init__(self, nombre):
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")

        self.__nombre = nombre
        self.__lotes = {}#Combiene más en diccionarios separados porque sino sería un diccionarios con listas
        self.__profesionales = {}#Y perdería sentido
        self.__equipos = {}
        self.__procedimientos = {}
        self.__administradores = {}

    def registrar_lote(self, lote):
        if lote.getter_id() in self.__lotes:
            raise ValueError("ID de lote duplicado")

        self.__lotes[lote.getter_id()] = lote

    def registrar_profesional(self, profesional):
        if profesional.getter_id() in self.__profesionales:
            raise ValueError("ID de profesional duplicado")

        self.__profesionales[profesional.getter_id()] = profesional

    def registrar_administrador(self, administrador):
        if administrador.getter_id() in self.__administradores:
            raise ValueError("ID de administrador duplicado")

        self.__administradores[administrador.getter_id()] = administrador

    def registrar_equipo(self, equipo):
        if equipo.getter_id() in self.__equipos:
            raise ValueError("ID de equipo duplicado")

        self.__equipos[equipo.getter_id()] = equipo

    def registrar_procedimiento(self, procedimiento):
        if procedimiento.getter_id() in self.__procedimientos:
            raise ValueError("ID de procedimiento duplicado")

        self.__procedimientos[procedimiento.getter_id()] = procedimiento

    def getter_lote(self, ID):
        return self.__lotes.get(ID)

    def getter_profesional(self, ID):
        return self.__profesionales.get(ID)

    def getter_equipo(self, ID):
        return self.__equipos.get(ID)

    def getter_procedimiento(self, ID):
        return self.__procedimientos.get(ID)