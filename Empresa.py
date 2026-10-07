class Empresa:
#La idea es que haya una única empresa o instancia que funcionará como un repertorio universal donde se añaden todos los profesionales, lotes, procedimientos, equipos y certificaciones
    def __init__(self, nombre):
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")

        self.nombre = nombre
        self.__lotes = {}#Combiene más en diccionarios separados porque sino sería un diccionarios con listas
        self.__profesionales = {}#Y perdería sentido
        self.__equipos = {}
        self.__procedimientos = {}

    def registrar_lote(self, lote):
        if lote.ID in self.__lotes:
            raise ValueError("ID de lote duplicado")

        self.__lotes[lote.ID] = lote

    def registrar_profesional(self, profesional):
        if profesional.ID in self.__profesionales:
            raise ValueError("ID de profesional duplicado")

        self.__profesionales[profesional.ID] = profesional

    def registrar_equipo(self, equipo):
        if equipo.ID in self.__equipos:
            raise ValueError("ID de equipo duplicado")

        self.__equipos[equipo.ID] = equipo

    def registrar_procedimiento(self, procedimiento):
        if procedimiento.ID in self.__procedimientos:
            raise ValueError("ID de procedimiento duplicado")

        self.__procedimientos[procedimiento.ID] = procedimiento

    def getter_lote(self, ID):
        return self.__lotes.get(ID)

    def getter_profesional(self, ID):
        return self.__profesionales.get(ID)

    def getter_equipo(self, ID):
        return self.__equipos.get(ID)

    def getter_procedimiento(self, ID):
        return self.__procedimientos.get(ID)