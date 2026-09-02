from datetime import date
from Profesional import Profesional 
from Equipo import Equipo
from Muestra import Muestra
from Procedimiento import Procedimiento
from Reporte import Reporte
class Inspeccion:
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

        elif not ID.isdigit():
            raise ValueError("El ID de la inspección debe ser un número entero.")

        else:
            self.ID = ID
            self.fecha = fecha
            self.profesional = profesional
            self.equipo = equipo
            self.procedimiento = procedimiento
            self.muestra = muestra

    def equipo_apto(self, equipo):
        if equipo.ultima_calibracion:
            return##########################################

# fecha_inspeccion - 6 meses <= fecha_calibracion <= fecha_inspeccion. Para este TP, seis meses se calculan como 182 días

    def ejecutar(self, Observaciones):
        if not isinstance(Observaciones, str):
            raise ValueError("Formato de Observaciones inválido.")
        else:##############################################
            return