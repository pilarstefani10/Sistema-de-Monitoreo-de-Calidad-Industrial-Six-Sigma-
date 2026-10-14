from Empleado import Empleado
from Lote import Lote
from datetime import date
from Inspeccion import Inspeccion
from ProcedimientoDimensional import ProcedimientoDimensional
from ProcedimientoVisual import ProcedimientoVisual
from Profesional import Profesional
from Equipo import Equipo
from Procedimiento import Procedimiento

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

    def crear_procedimiento(self,tipo,*args,**kwargs):
        tipo=tipo.upper()
        if tipo == "DIMENSIONAL":
            procedimiento = ProcedimientoDimensional(*args, **kwargs)

        elif tipo == "VISUAL":
            procedimiento = ProcedimientoVisual(*args, **kwargs)

        else:
            raise ValueError("Tipo de procedimiento inválido")#############ERROR A PERSONALIZARRRR

        self.__empresa.registrar_procedimiento(procedimiento)

        return procedimiento

    def crear_muestra(self, id_lote, unidades, id_profesional, id_equipo, id_procedimiento):
        lote = self.__empresa.buscar_lote(id_lote)
        profesional = self.__empresa.buscar_profesional(id_profesional)
        equipo = self.__empresa.buscar_equipo(id_equipo)
        procedimiento = self.__empresa.buscar_procedimiento(id_procedimiento)
        fecha = date.today()
        
        Inspeccion.validar(fecha, profesional, equipo, procedimiento)

        muestra = lote.crear_muestra(unidades)
        self.crear_inspeccion(muestra,fecha,profesional,equipo,procedimiento)
        
        return muestra

    def crear_inspeccion(self, muestra, fecha, profesional, equipo, procedimiento):
            inspeccion = Inspeccion(
                muestra.getter_id(),
                fecha,
                profesional,
                equipo,
                procedimiento,
                muestra
            )

            muestra.setter_inspeccion(inspeccion)
            profesional.asignar_inspeccion(inspeccion)

            return inspeccion

    def evaluar_lote(self, id_lote):
        lote = self.__empresa.buscar_lote(id_lote)
        lote.decidir_estado()
        return lote.getter_estado()

    def getter_empresa(self):
        return self.__empresa

    