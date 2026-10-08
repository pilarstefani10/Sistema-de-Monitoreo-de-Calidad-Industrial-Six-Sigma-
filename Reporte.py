from datetime import date
from Profesional import Profesional
from Muestra import Muestra
from Lote import Lote

class Reporte:

    def __init__(self, ID, inspeccion):
        muestra = inspeccion.getter_muestra()

        if muestra.getter_estado() != "NO_CONFORME":
            raise ValueError("Solo se generan reportes para muestras No Conformes.")

        self.__ID = ID
        self.__inspeccion = inspeccion
        self.__defectos = muestra.getter_defectos()

    def crear_resumen(self):
        muestra = self.__inspeccion.getter_muestra()

        resumen = "\nReporte: " + self.__ID + "\n"
        resumen += "Fecha: " + str(self.__inspeccion.getter_fecha()) + "\n"
        resumen += "Muestra: " + muestra.getter_id() + "\n"
        resumen += "Lote: " + muestra.getter_lote().getter_id() + "\n"
        resumen += "Responsable: " + self.__inspeccion.getter_profesional().getter_nombre() + "\n"

        for numero, defecto in enumerate(self.__defectos, start=1):
            resumen += str(numero) + ". Tipo: " + defecto.getter_tipo()
            resumen += " | Descripción: " + defecto.getter_descripcion()
            resumen += " | Gravedad: " + str(defecto.getter_gravedad()) + "\n"

        return resumen

    def getter_id(self):
        return self.__ID

    def getter_inspeccion(self):
        return self.__inspeccion

    def getter_defectos(self):
        return self.__defectos.copy()