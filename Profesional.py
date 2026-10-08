from Certificacion import Certificacion
from random import random


class Profesional:
    nextid = 1

    profesionales = []  # Lista para almacenar todas las instancias de Profesional
    
    def __init__(self, name):
        if not self.validar_nombre(name):
            raise ValueError("El nombre del profesional no puede estar vacío.")
        else:
            self.__name = name
            self.__ID = "P" + str(Profesional.nextid)
            Profesional.profesionales.append(self)
            Profesional.nextid += 1
            self.__certificaciones = []

    @staticmethod
    def validar_nombre(nombre):
        return isinstance(nombre, str) and nombre != ""

    def agregar_certificacion(self, certificacion):
        if not isinstance(certificacion, Certificacion):
            raise ValueError("El objeto proporcionado no es una instancia de la clase Certificacion.")
        self.__certificaciones.append(certificacion)


    def certificacion_vigente(self, nombre_certificacion, fecha):
        return any(map(lambda cert: cert.getter_nombre() == nombre_certificacion and cert.esta_vigente(fecha),self.__certificaciones))
        
    
    @classmethod
        
    def buscar_profesional(cls, nombre, ID):
        encontrados = filter(lambda profesional: profesional.getter_nombre() == nombre and profesional.getter_id() == ID, cls.profesionales)
        return next(encontrados, None)




    
    def __str__(self):
        return f"Profesional: {self.__name}, ID: {self.__ID}, Certificaciones: {[cert.getter_nombre() for cert in self.__certificaciones]}"  
    
    def obtener_inspecciones(self, muestras):
        muestras_del_profesional = filter(
            lambda muestra: muestra.getter_inspeccion() is not None
            and muestra.getter_inspeccion().getter_profesional() == self,
            muestras
        )

        return list(
            map(
                lambda muestra: muestra.getter_inspeccion(),
                muestras_del_profesional
            )
        )

    def getter_id(self):
        return self.__ID

    def getter_nombre(self):
        return self.__name