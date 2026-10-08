from datetime import date, timedelta
from Profesional import Profesional 
from Equipo import Equipo
from Procedimiento import Procedimiento
class Inspeccion:

    inspecciones = []

    def __init__(self, ID, fecha, profesional, equipo, procedimiento, muestra):
        if not isinstance(fecha, date):
            raise ValueError("La fecha debe ser un objeto de tipo date.")

        elif not isinstance(profesional, Profesional):
            raise ValueError("El profesional debe ser una instancia de la clase Profesional.")

        elif not isinstance(equipo, Equipo): 
            raise ValueError("El equipo debe ser una instancia de la clase Equipo.")

        elif not isinstance(procedimiento, Procedimiento):
            raise ValueError("El procedimiento debe ser una instancia de la clase Procedimiento.")

        elif not profesional.certificacion_vigente(procedimiento.getter_certificacion_requerida(), fecha):
            raise ValueError("El profesional no tiene la certificación requerida vigente para este procedimiento.")

        elif not (
            fecha - timedelta(days=182)
            <= equipo.getter_ultima_calibracion()
            <= fecha
            and equipo.getter_categoria() == procedimiento.getter_categoria_equipo()
        ):
            raise ValueError("El equipo no es apto para realizar la inspección según el procedimiento y la fecha de calibración.")

        else:
            self.__ID =  str(ID) + "I"
            self.__fecha = fecha
            self.__profesional = profesional
            self.__equipo = equipo
            self.__procedimiento = procedimiento
            self.__muestra = muestra
            self.reporte=None

    def equipo_apto(self):

        fecha_limite = self.__fecha - timedelta(days=182)

        calibracion_ok = (fecha_limite <= self.__equipo.getter_ultima_calibracion() <= self.__fecha)
        categoria_ok = (
            self.__equipo.getter_categoria()
            == self.__procedimiento.getter_categoria_equipo()
        )

        return calibracion_ok and categoria_ok

    def __str__(self):
        return f"Inspección {self.__ID} - Fecha: {self.__fecha} - Profesional: {self.__profesional.getter_nombre()} - Equipo: {self.__equipo.getter_id()} - Procedimiento: {self.__procedimiento.getter_nombre()} - Muestra: {self.__muestra.getter_id()}"


    def ejecutar(self):

        defectos = []
        
        for i in range(self.__muestra.getter_unidadesrepresentadas()):

            defecto = self.__procedimiento.evaluar_unidad()

            if defecto is not None:
                defectos.append(defecto)

        self.__muestra.iniciar_inspeccion()
        self.__muestra.registrar_defectos(defectos)

        self.__muestra.cerrar()
        return

    def conformidad(self):
        defectos = self.__muestra.getter_defectos()
        
        gravedad_total = 0
        hay_defecto_critico = False

        gravedad_total= sum(map(lambda defecto: defecto.getter_gravedad(),
                                 defectos))

        hay_defecto_critico = any(
            map(lambda defecto: defecto.es_critico(), defectos))

        if hay_defecto_critico or gravedad_total > self.__procedimiento.getter_limitegravedad():
            self.
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
