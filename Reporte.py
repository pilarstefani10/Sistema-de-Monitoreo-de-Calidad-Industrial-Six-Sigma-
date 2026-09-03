from datetime import date
from Profesional import Profesional
from Muestra import Muestra
from Lote import Lote
from Inspeccion import Inspeccion

class Reporte:
    def __init__(self, ID, fecha, muestra, lote, profesional):
        if not isinstance(fecha, date):
            raise ValueError("La fecha debe ser un objeto de tipo date.")
        
        elif not isinstance(profesional, Profesional):
            raise ValueError("El profesional debe ser una instancia de la clase Profesional.")
        
        elif not isinstance(muestra, Muestra):
            raise ValueError("La muestra debe ser una instancia de la clase Muestra.")
        
        elif not ID.isdigit():
            raise ValueError("El ID de la inspección debe ser un número entero.")
        
        elif not isinstance(lote,Lote):
            raise ValueError("El lote debe ser una instancia de la clase Lote.")
        

        self.ID = ID
        self.fecha = fecha
        self.muestra = muestra
        self.lote = lote
        self.responsables = profesional
        self.causas = muestra.defectos

    def crear_resumen(self):
        Resumen="\nReporte"+ str(self.ID)+'\n'
        Resumen+="Fecha:"+str(self.fecha)+'\n'
        Resumen+="Muestra:"+str(self.muestra.ID)+'\n'
        Resumen+="Responsable:"+str(self.responsables.name)+'\n'
        for i in range(len(self.muestra.defectos)):
            defecto = self.muestra.defectos[i]

            Resumen += str(i + 1) + ". "
            Resumen += "Tipo: " + defecto.tipo
            Resumen += " | Descripción: " + defecto.descripcion
            Resumen += " | Gravedad: " + str(defecto.gravedad)
            Resumen += "\n"

        return Resumen   

