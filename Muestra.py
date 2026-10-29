from Defecto import Defecto
from Inspeccion import Inspeccion
from Excepciones import DatosInvalidosError,TransicionInvalidaError
class Muestra:

    def __init__(self, ID, unidades_representadas, lote):

        if not isinstance(unidades_representadas, int) or unidades_representadas <= 0:
            raise DatosInvalidosError(
                "Las unidades representadas deben ser enteros mayores a cero"
            )

        self.__ID = ID
        self.__unidades_representadas = unidades_representadas
        self.__inspeccion=None
        self.__estado = "PENDIENTE"
        self.__lote = lote
        self.__defectos = []

    def registrar_defectos(self, defectos):

        if not isinstance(defectos, list):
            raise DatosInvalidosError(
                "Los defectos deben ingresarse en una lista."
            )

        elif self.__estado in ["CONFORME", "NO_CONFORME"]:
            raise TransicionInvalidaError(
                "No se pueden agregar defectos a una muestra cerrada."
            )

        else:
            if not all(map(lambda defecto: isinstance(defecto, Defecto), defectos)):
                raise DatosInvalidosError( "Todos los elementos de la lista deben ser objetos de tipo Defecto.")
    
            self.__defectos.extend(defectos)

    def iniciar_inspeccion(self):
        if self.__estado != "PENDIENTE":
            raise TransicionInvalidaError("La muestra ya fue inspeccionada.")
        elif self.__inspeccion is None:
            raise TransicionInvalidaError("La muestra no tiene una inspección asignada.")
        else:
            self.__estado = "EN_INSPECCION"

    def cerrar(self):
        if self.__estado != "EN_INSPECCION":
            raise TransicionInvalidaError("La muestra no está en inspección.")

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

    def setter_inspeccion(self, inspeccion):
        if self.__estado != "PENDIENTE":
            raise TransicionInvalidaError("La muestra ya inició su inspección")

        if self.__inspeccion is not None:
            raise TransicionInvalidaError("La muestra ya tiene una inspección asignada")

        if not isinstance(inspeccion, Inspeccion):
            raise DatosInvalidosError("Debe asignarse una inspección válida")

        if inspeccion.getter_muestra() is not self:
            raise DatosInvalidosError("La inspección pertenece a otra muestra")

        self.__inspeccion = inspeccion

    def getter_lote(self):
        return self.__lote

    def getter_id(self):
        return self.__ID

    