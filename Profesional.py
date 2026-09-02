from Certificacion import Certificacion
class Profesional:
    def __init__(self, name, id):
        if not self.validar_nombre(name):
            raise ValueError("El nombre del profesional no puede estar vacío.")
        elif not self.validar_id(id):
            raise ValueError("El ID del profesional no puede estar vacío.")
        else:
            self.name = name
            self.ID = id
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
    
    
