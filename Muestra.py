from Defecto import Defecto
from Inspeccion import Inspeccion
from Profesional import Profesional
from Equipo import Equipo
from Procedimiento import Procedimiento
from datetime import date
class Muestra:

    def __init__(self, ID, unidades_representadas, lote):

        if unidades_representadas <= 0:
            raise ValueError(
                "Las unidades representadas deben ser mayores a cero"
            )

        self.ID = ID
        self.unidades_representadas = unidades_representadas
        self.inspeccion=None
        self.estado = "PENDIENTE"
        self.lote = lote
        self.defectos = []


    def crear_inspeccion(self, fecha, profesional, equipo, procedimiento):

        if self.estado != "PENDIENTE":
            raise ValueError(
                "Solo se puede inspeccionar una muestra pendiente."
            )

        elif self.inspeccion is not None:
            raise ValueError(
                "La muestra ya posee una inspección."
            )

        elif not isinstance(fecha, date):
            raise ValueError(
                "La fecha debe ser un objeto de tipo date."
            )

        elif not isinstance(profesional, Profesional):
            raise ValueError(
                "El profesional debe ser una instancia de la clase Profesional."
            )

        elif not isinstance(equipo, Equipo):
            raise ValueError(
                "El equipo debe ser una instancia de la clase Equipo."
            )

        elif not isinstance(procedimiento, Procedimiento):
            raise ValueError(
                "El procedimiento debe ser una instancia de la clase Procedimiento."
            )

        else:
            self.inspeccion = Inspeccion(
                self.ID,
                fecha,
                profesional,
                equipo,
                procedimiento,
                self
            )

            return self.inspeccion

    def registrar_defectos(self, defectos):

        if not isinstance(defectos, list):
            raise ValueError(
                "Los defectos deben ingresarse en una lista."
            )

        elif self.estado in ["CONFORME", "NO_CONFORME"]:
            raise ValueError(
                "No se pueden agregar defectos a una muestra cerrada."
            )

        else:
            for defecto in defectos:
                if not isinstance(defecto, Defecto):
                    raise ValueError(
                        "Todos los elementos de la lista deben ser objetos de tipo Defecto."
                    )

            self.defectos.extend(defectos)
        