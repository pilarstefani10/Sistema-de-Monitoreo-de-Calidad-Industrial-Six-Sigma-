from Empleado import Empleado
from Lote import Lote
from datetime import date
from Inspeccion import Inspeccion
from ProcedimientoDimensional import ProcedimientoDimensional
from ProcedimientoVisual import ProcedimientoVisual
from Profesional import Profesional
from Equipo import Equipo
from Procedimiento import Procedimiento
from datetime import date, timedelta

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

    def crear_muestra(self, lote, unidades ,id_profesional, id_equipo, id_procedimiento):
        profesional = self.__empresa.getter_profesional(id_profesional)
        equipo=self.__empresa.getter_equipo(id_equipo)
        procedimiento=self.__empresa.getter_procedimiento(id_procedimiento)
        muestra= lote.crear_muestra(unidades)
        fecha = date.today()
        self.validar_inspeccion(
            fecha,
            profesional,
            equipo,
            procedimiento)
        
        inspeccion= self.crear_inspeccion(muestra,fecha,profesional,equipo,procedimiento)
        
        muestra.setter_inspeccion(inspeccion)
        
        profesional.asignar_inspeccion(inspeccion)
        
        return muestra

    def crear_procedimiento(self,tipo,*args,**kwargs):
        tipo=tipo.upper()
        if tipo == "DIMENSIONAL":
            procedimiento = ProcedimientoDimensional(*args, **kwargs)

        elif tipo == "VISUAL":
            procedimiento = ProcedimientoVisual(*args, **kwargs)

        else:
            raise ValueError("Tipo de procedimiento inválido")#############ERROR A PERSONALIZARRRR

        if self.__empresa.getter_procedimiento(procedimiento.getter_id())!=None:
            raise ValueError("Ya existe un procedimiento con ese ID")###############ERROR A PERSONALIZARRR

        self.__empresa.registrar_procedimiento(procedimiento)

        return procedimiento

    @staticmethod
    def crear_inspeccion(muestra, fecha, profesional, equipo, procedimiento):
            inspeccion = Inspeccion(
                muestra.getter_id(),
                fecha,
                profesional,
                equipo,
                procedimiento,
                muestra
            )

            return inspeccion

    @staticmethod
    def validar_inspeccion(fecha, profesional, equipo, procedimiento):

        if not isinstance(fecha, date):
            raise ValueError("La fecha debe ser de tipo date")

        if not isinstance(profesional, Profesional):
            raise ValueError("El profesional no es válido")

        if not isinstance(equipo, Equipo):
            raise ValueError("El equipo no es válido")

        if not isinstance(procedimiento, Procedimiento):
            raise ValueError("El procedimiento no es válido")

        if not profesional.certificacion_vigente(
            procedimiento.getter_certificacion_requerida(), fecha
        ):
            raise ValueError(
                "El profesional no tiene la certificación vigente"
            )

        if not (
            fecha - timedelta(days=182)
            <= equipo.getter_ultima_calibracion()
            <= fecha
        ):
            raise ValueError(
                "El equipo no tiene una calibración vigente"
            )

        if equipo.getter_categoria() != procedimiento.getter_categoria_equipo():
            raise ValueError(
                "La categoría del equipo no coincide con el procedimiento"
            )

    def getter_empresa(self):
        return self.__empresa

    