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

        elif not profesional.certificacion_vigente(procedimiento.certificacion_requerida, fecha):
            raise ValueError("El profesional no tiene la certificación requerida vigente para este procedimiento.")

        elif not (
            fecha - timedelta(days=182)
            <= equipo.ultima_calibracion
            <= fecha
            and equipo.categoria == procedimiento.categoria_equipo_requerida
        ):
            raise ValueError("El equipo no es apto para realizar la inspección según el procedimiento y la fecha de calibración.")

        else:
            self.ID =  str(ID) + "I"
            self.fecha = fecha
            self.profesional = profesional
            self.equipo = equipo
            self.procedimiento = procedimiento
            self.muestra = muestra

    def equipo_apto(self):

        fecha_limite = self.fecha - timedelta(days=182)

        calibracion_ok = (fecha_limite <= self.equipo.ultima_calibracion <= self.fecha)
        categoria_ok = (
            self.equipo.categoria
            == self.procedimiento.categoria_equipo_requerida
        )

        return calibracion_ok and categoria_ok

    def __str__(self):
        return f"Inspección {self.ID} - Fecha: {self.fecha} - Profesional: {self.profesional.name} - Equipo: {self.equipo.ID} - Procedimiento: {self.procedimiento.nombre} - Muestra: {self.muestra.ID}"
    

    def ejecutar(self):

        defectos = []
        
        for i in range(self.muestra.getter_unidadesrepresentadas()):

            defecto = self.procedimiento.evaluar_unidad()

            if defecto is not None:
                defectos.append(defecto)

        self.muestra.registrar_defectos(defectos)

        return

    def conformidad(self):
        defectos = self.muestra.getter_defectos
        
        gravedad_total = 0
        hay_defecto_critico = False

        for d in defectos:
            gravedad_total += d.getter_gravedad()

            if d.gravedad == 5:
                hay_defecto_critico = True

        if hay_defecto_critico or gravedad_total >= self.procedimiento.getter_limitegravedad():
            return False
        else:
            return True

