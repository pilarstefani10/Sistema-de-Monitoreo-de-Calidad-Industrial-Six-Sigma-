from Empleado import Empleado
from Lote import Lote
from datetime import date
from Inspeccion import Inspeccion
from ProcedimientoDimensional import ProcedimientoDimensional
from ProcedimientoVisual import ProcedimientoVisual

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

    def crear_muestra(self, lote, id_profesional, id_equipo, id_procedimiento):
        profesional = self.__empresa.getter_profesional(id_profesional)
        equipo=self.__empresa.getter_equipo(id_equipo)
        procedimiento=self.__empresa.getter_procedimiento(id_procedimiento)
        muestra= lote.crear_muestra()
        fecha = date.today()
        inspeccion= muestra.crear_inspeccion(fecha,profesional,equipo,procedimiento)
        return muestra, inspeccion

    def crear_procedimiento(self,tipo,*args,**kwargs):

        if tipo == "DIMENSIONAL":
            procedimiento = ProcedimientoDimensional(*args, **kwargs)

        elif tipo == "VISUAL":
            procedimiento = ProcedimientoVisual(*args, **kwargs)

        else:
            raise ValueError("Tipo de procedimiento inválido")

        if self.__empresa.getter_procedimiento(procedimiento.ID)!=None:
            raise ValueError("Ya existe un procedimiento con ese ID")

        self.__procedimientos[procedimiento.ID] = procedimiento

        return procedimiento


    def crear_inspeccion(self, fecha, profesional, equipo, procedimiento):
            self.__inspeccion = Inspeccion(
                self.__ID,
                fecha,
                profesional,
                equipo,
                procedimiento,
                self
            )

            return self.__inspeccion

    def getter_empresa(self):
        return self.__empresa

    