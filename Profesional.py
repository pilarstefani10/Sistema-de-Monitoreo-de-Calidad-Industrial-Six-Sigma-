from Certificacion import Certificacion
from random import random


class Profesional:
    nextid = 1

    profesionales = []  # Lista para almacenar todas las instancias de Profesional
    
    def __init__(self, name):
        if not self.validar_nombre(name):
            raise ValueError("El nombre del profesional no puede estar vacío.")
        else:
            self.name = name
            self.ID = "P" + str(Profesional.nextid)
            Profesional.profesionales.append(self)
            Profesional.nextid += 1
            self.certificaciones = []

    @staticmethod
    def validar_nombre(nombre):
        return isinstance(nombre, str) and nombre != ""

    def agregar_certificacion(self, certificacion):
        if not isinstance(certificacion, Certificacion):
            raise ValueError("El objeto proporcionado no es una instancia de la clase Certificacion.")
        self.certificaciones.append(certificacion)

    def certificacion_vigente(self, nombre_certificacion, fecha):
        for cert in self.certificaciones:
            if cert.name == nombre_certificacion and cert.esta_vigente(fecha):
                return True
        return False

    @classmethod
    def buscar_profesional(cls, nombre, ID):

        for profesional in cls.profesionales:

            if profesional.name == nombre and profesional.ID == ID:
                return profesional

        return None



    
    def __str__(self):
        return f"Profesional: {self.name}, ID: {self.ID}, Certificaciones: {[cert.name for cert in self.certificaciones]}"  
    
    def obtener_inspecciones(self, muestras):
        inspecciones = []

        for muestra in muestras:
            if muestra.inspeccion.profesional == self:
                inspecciones.append(muestra.inspeccion)

        return inspecciones