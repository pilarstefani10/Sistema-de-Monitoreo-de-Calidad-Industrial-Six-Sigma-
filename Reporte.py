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
        
        elif not isinstance(lote,Lote):
            raise ValueError("El lote debe ser una instancia de la clase Lote.")
        

        self.__ID = ID
        self.__fecha = fecha
        self.__muestra = muestra
        self.__lote = lote
        self.__responsables = profesional
        self.__causas = muestra.getter_defectos()

    def crear_resumen(self):
        Resumen="\nReporte"+ str(self.__ID)+'\n'
        Resumen+="Fecha:"+str(self.__fecha)+'\n'
        Resumen+="Muestra:"+str(self.__muestra.getter_id())+'\n'
        Resumen+="Responsable:"+str(self.__responsables.getter_nombre())+'\n'
        for i in range(len(self.__causas)):
            defecto = self.__causas[i]

            Resumen += str(i + 1) + ". "
            Resumen += "Tipo: " + defecto.getter_tipo()
            Resumen += " | Descripción: " + defecto.getter_descripcion()
            Resumen += " | Gravedad: " + str(defecto.getter_gravedad())
            Resumen += "\n"

        return Resumen   

    @classmethod
    def crear_desde_inspeccion(cls, ID, inspeccion):

        muestra = inspeccion.getter_muestra()

        return cls(
            ID,
            inspeccion.getter_fecha(),
            muestra,
            muestra.getter_lote(),
            inspeccion.getter_profesional()
        )
        
    def getter_id(self):
        return self.__ID
