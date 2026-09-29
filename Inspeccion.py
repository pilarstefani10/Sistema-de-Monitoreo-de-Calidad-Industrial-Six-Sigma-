from datetime import date, timedelta
from Profesional import Profesional 
from Equipo import Equipo
from Procedimiento import Procedimiento
from Defecto import Defecto
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
    

    def ejecutar(self, defectos, observaciones):
        if not isinstance(observaciones, str):
            raise ValueError("Formato de observaciones inválido.")

        if not isinstance(defectos, list):
            raise ValueError("Los defectos deben ingresarse en una lista.")

        for defecto in defectos:
            if not isinstance(defecto, Defecto):
                raise ValueError("Todos los elementos deben ser objetos Defecto.")

        self.muestra.defectos = defectos

        gravedad_total = 0
        hay_defecto_critico = False

        for defecto in defectos:
            gravedad_total += defecto.gravedad

            if defecto.gravedad == 5:
                hay_defecto_critico = True

        if hay_defecto_critico or gravedad_total >= 5:
            self.muestra.estado = "RECHAZADO"
        else:
            self.muestra.estado = "APROBADO"

        return defectos