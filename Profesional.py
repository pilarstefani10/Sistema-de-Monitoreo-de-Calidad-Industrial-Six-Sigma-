from Certificacion import Certificacion
class Profesional:
    nextid = 1
    def __init__(self, name):
        if not self.validar_nombre(name):
            raise ValueError("El nombre del profesional no puede estar vacío.")
        else:
            self.name = name
            self.ID = "P" + str(Profesional.nextid)
            Profesional.nextid += 1
            self.certificaciones = []

    @staticmethod
    def validar_id(id_profesional):
        return isinstance(id_profesional, str) and id_profesional != ""

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
    def __str__(self):
        return f"Profesional: {self.name}, ID: {self.ID}, Certificaciones: {[cert.name for cert in self.certificaciones]}"  
    
