from Empleado import Empleado
from Lote import Lote


class Administrador(Empleado):
    nextid = 1

    def __init__(self, name, empresa):
        super().__init__(name, "A" + str(Administrador.nextid))
        Administrador.nextid += 1
        self.__empresa = empresa
        empresa.registrar_administrador(self)

    def crear_lote(self, cantidad_fabricada):
        lote = Lote(cantidad_fabricada)
        self.__empresa.registrar_lote(lote)
        return lote

    def registrar_profesional(self, profesional):
        self.__empresa.registrar_profesional(profesional)

    def registrar_equipo(self, equipo):
        self.__empresa.registrar_equipo(equipo)

    def registrar_procedimiento(self, procedimiento):
        self.__empresa.registrar_procedimiento(procedimiento)

    def crear_muestra(self, lote, fecha, profesional, equipo, procedimiento):
        profesional = empresa.obtener profesional(id profesional)
        muestra= lote.crear muestra
        crear inspeccion
        return lote.crear_muestra(fecha, profesional, equipo, procedimiento)

    def getter_empresa(self):
        return self.__empresa