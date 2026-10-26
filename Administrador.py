from Empleado import Empleado
from Lote import Lote
from datetime import date
from Inspeccion import Inspeccion
from ProcedimientoDimensional import ProcedimientoDimensional
from ProcedimientoVisual import ProcedimientoVisual
from Profesional import Profesional
from Equipo import Equipo
from Muestra import Muestra
from Excepciones import DatosInvalidosError

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

    def crear_profesional(self, nombre):
        profesional = Profesional(nombre)
        self.__empresa.registrar_profesional(profesional)
        return profesional

    def crear_equipo(self, categoria, ultima_calibracion):
        equipo = Equipo(categoria, ultima_calibracion)
        self.__empresa.registrar_equipo(equipo)
        return equipo

    def crear_procedimiento(self,tipo,*args,**kwargs):
        tipo=tipo.upper()
        if tipo == "DIMENSIONAL":
            procedimiento = ProcedimientoDimensional(*args, **kwargs)

        elif tipo == "VISUAL":
            procedimiento = ProcedimientoVisual(*args, **kwargs)

        else:
            raise DatosInvalidosError("Tipo de procedimiento inválido")

        self.__empresa.registrar_procedimiento(procedimiento)

        return procedimiento

    def crear_muestra(self, id_lote, unidades, id_profesional, id_equipo, id_procedimiento):
        lote = self.__empresa.buscar_lote(id_lote)
        profesional = self.__empresa.buscar_profesional(id_profesional)
        equipo = self.__empresa.buscar_equipo(id_equipo)
        procedimiento = self.__empresa.buscar_procedimiento(id_procedimiento)
        fecha = date.today()
        
        Inspeccion.validar(fecha, profesional, equipo, procedimiento)

        lote.validar_extraccion(unidades)
        muestra = Muestra(lote.proximo_id_muestra(), unidades, lote)
        lote.agregar_muestra(muestra)

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
        resultado = lote.resultado_segun_criterio()
        lote.registrar_resultado(resultado)
        return resultado

    def comparar_lotes(self, id_lote1, id_lote2):
        if id_lote1 == id_lote2:
            raise ValueError("Debe elegir dos lotes distintos.")
        tipos1 = self.__empresa.buscar_lote(id_lote1).tipos_defectos_dimensionales()
        tipos2 = self.__empresa.buscar_lote(id_lote2).tipos_defectos_dimensionales()
        return tipos1 & tipos2, tipos1 - tipos2, tipos2 - tipos1

    def getter_empresa(self):
        return self.__empresa

    