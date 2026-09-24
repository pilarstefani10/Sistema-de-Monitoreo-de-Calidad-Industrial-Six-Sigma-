from Defecto import Defecto 
from Inspeccion import Inspeccion

class Muestra:

    def __init__(self, ID, unidades_representadas, lote, date, profesional, equipo, procedimiento):

        if unidades_representadas <= 0:
            raise ValueError(
                "Las unidades representadas deben ser mayores a cero"
            )

        self.ID = ID
        self.unidades_representadas = unidades_representadas

        self.estado = "PENDIENTE"
        self.lote = lote
        self.defectos = []

        self.inspeccion = Inspeccion(
            self.ID,
            date,
            profesional,
            equipo,
            procedimiento,
            self)


    def registrar_defecto(self, defecto):

        if not isinstance(defecto, Defecto):
            raise ValueError("Se debe ingresar un objeto de tipo Defecto")

        self.defectos.append(defecto)
        