from datetime import date, timedelta
from Profesional import Profesional 
from Equipo import Equipo
from Muestra import Muestra
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

        elif not isinstance(muestra, Muestra):
            raise ValueError("La muestra debe ser una instancia de la clase Muestra.")

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
    
    def ejecutar(self, Observaciones): #Funcionalidad incompleta, solo boceto del futuro
        if not isinstance(Observaciones, str):
            raise ValueError("Formato de Observaciones inválido.")
        else:###########################################################
            self.muestra.defectos.append(self.defecto)
            return