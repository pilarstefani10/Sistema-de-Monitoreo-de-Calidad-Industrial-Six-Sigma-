from Defecto import Defecto
from Inspeccion import Inspeccion
from Profesional import Profesional
from Equipo import Equipo
from Procedimiento import Procedimiento
from datetime import date
class Muestra:

    def __init__(self, ID, unidades_representadas, lote):

        if unidades_representadas <= 0 or not isinstance(unidades_representadas, int):
            raise ValueError(
                "Las unidades representadas deben ser enteros mayores a cero"
            )

        self.__ID = ID
        self.__unidades_representadas = unidades_representadas
        self.__inspeccion=None
        self.__estado = "PENDIENTE"
        self.__lote = lote
        self.__defectos = []

    """""
    def crear_inspeccion(self, fecha, profesional, equipo, procedimiento):

        if self.__estado != "PENDIENTE":
            raise ValueError(
                "Solo se puede inspeccionar una muestra pendiente."
            )

        elif self.__inspeccion is not None:
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
            
            self.__inspeccion = Inspeccion(
                self.__ID,
                fecha,
                profesional,
                equipo,
                procedimiento,
                self
            )

            return self.__inspeccion"""

    def registrar_defectos(self, defectos):

        if not isinstance(defectos, list):
            raise ValueError(
                "Los defectos deben ingresarse en una lista."
            )

        elif self.__estado in ["CONFORME", "NO_CONFORME"]:
            raise ValueError(
                "No se pueden agregar defectos a una muestra cerrada."
            )

        else:
            if not all(map(lambda defecto: isinstance(defecto, Defecto), defectos)):
                raise ValueError( "Todos los elementos de la lista deben ser objetos de tipo Defecto.")
    
            self.__defectos.extend(defectos)

    def iniciar_inspeccion(self):
        if self.__estado != "PENDIENTE":
            raise ValueError("La muestra ya fue inspeccionada.")
        elif self.__inspeccion is None:
            raise ValueError("La muestra no tiene una inspección asignada.")
        else:
            self.__estado = "EN_INSPECCION"

    def cerrar(self):
        if self.__estado != "EN_INSPECCION":
            raise ValueError("La muestra no está en inspección.")

        if self.__inspeccion.conformidad():
            self.__estado="CONFORME"
        else:
            self.__estado ="NO_CONFORME"

    #Getters y Setters
    def getter_unidadesrepresentadas(self):
        return self.__unidades_representadas

    def getter_defectos(self):
        return self.__defectos.copy()

    def getter_estado(self):
        return self.__estado

    def getter_inspeccion(self):
        return self.__inspeccion

    def getter_lote(self):
        return self.__lote

    def getter_id(self):
        return self.__ID

    