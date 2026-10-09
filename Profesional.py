from Certificacion import Certificacion
from random import random
from Empleado import Empleado


class Profesional(Empleado):
    nextid = 1

    profesionales = []  # Lista para almacenar todas las instancias de Profesional
    
    def __init__(self, name):
        super().__init__(name, "P" + str(Profesional.nextid))
        Profesional.profesionales.append(self)
        Profesional.nextid += 1
        self.__certificaciones = []

    def agregar_certificacion(self, certificacion):
        if not isinstance(certificacion, Certificacion):
            raise ValueError("El objeto proporcionado no es una instancia de la clase Certificacion.")
        self.__certificaciones.append(certificacion)


    def certificacion_vigente(self, nombre_certificacion, fecha):
        return any(map(lambda cert: cert.getter_nombre() == nombre_certificacion and cert.esta_vigente(fecha),self.__certificaciones))
        

    def __str__(self):
        return f"Profesional: {self.getter_nombre()}, ID: {self.getter_id()}, Certificaciones: {[cert.getter_nombre() for cert in self.__certificaciones]}"  
    
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

    