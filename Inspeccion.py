from datetime import date, timedelta
from Profesional import Profesional 
from Equipo import Equipo
from Procedimiento import Procedimiento
from Excepciones import DatosInvalidosError,EquipoNoAptoError,CertificacionInvalidaError,TransicionInvalidaError
class Inspeccion:

    def __init__(self, ID, fecha, profesional, equipo, procedimiento, muestra):
        
        Inspeccion.validar(fecha, profesional, equipo, procedimiento)

        self.__ID = str(ID) + "I"
        self.__fecha = fecha
        self.__profesional = profesional
        self.__equipo = equipo
        self.__procedimiento = procedimiento
        self.__muestra = muestra
        self.__reporte = None

    @staticmethod
    def validar(fecha, profesional, equipo, procedimiento):

        if not isinstance(fecha, date):
            raise DatosInvalidosError("La fecha debe ser de tipo date")

        if not isinstance(profesional, Profesional):
            raise DatosInvalidosError("El profesional no es válido")

        if not isinstance(equipo, Equipo):
            raise DatosInvalidosError("El equipo no es válido")

        if not isinstance(procedimiento, Procedimiento):
            raise DatosInvalidosError("El procedimiento no es válido")

        faltantes = profesional.certificaciones_faltantes(procedimiento.getter_certificaciones_requeridas(), fecha)
        if faltantes:
            raise CertificacionInvalidaError("Al profesional " + profesional.getter_nombre() + " le faltan las certificaciones: " + ", ".join(sorted(faltantes)))


        if not equipo.calibracion_vigente(fecha):
            raise EquipoNoAptoError("El equipo no tiene una calibración vigente")

        if equipo.getter_categoria() != procedimiento.getter_categoria_equipo():
            raise EquipoNoAptoError("La categoría del equipo no coincide con el procedimiento")   

    def __str__(self):
        return f"Inspección {self.__ID} - Fecha: {self.__fecha} - Profesional: {self.__profesional.getter_nombre()} - Equipo: {self.__equipo.getter_id()} - Procedimiento: {self.__procedimiento.getter_nombre()} - Muestra: {self.__muestra.getter_id()}"

    def registrar_reporte(self, reporte):
        if self.__muestra.getter_estado() != "NO_CONFORME":
            raise TransicionInvalidaError("Solo se registran reportes de muestras No Conformes.")
        if self.__reporte is not None:
            raise TransicionInvalidaError("La inspección ya tiene un reporte.")
        self.__reporte = reporte

    def conformidad(self):
        defectos = self.__muestra.getter_defectos()
        
        gravedad_total = 0
        hay_defecto_critico = False

        gravedad_total= sum(map(lambda defecto: defecto.getter_gravedad(),
                                 defectos))

        hay_defecto_critico = any(
            map(lambda defecto: defecto.es_critico(), defectos))

        if hay_defecto_critico or gravedad_total > self.__procedimiento.getter_limitegravedad():
            return False
        else:
            return True

    def getter_fecha(self):
        return self.__fecha

    def getter_profesional(self):
        return self.__profesional

    def getter_equipo(self):
        return self.__equipo

    def getter_procedimiento(self):
        return self.__procedimiento

    def getter_muestra(self):
        return self.__muestra

    def getter_id(self):
        return self.__ID

    def getter_reporte(self):
        return self.__reporte