
from Excepciones import DatosInvalidosError
class Procedimiento:
    nextid = 1
    def __init__(self, nombre, categoria_equipo_requerida, certificaciones_requeridas, limite_gravedad):
        if not isinstance(nombre, str) or nombre == "":
            raise DatosInvalidosError("El nombre del procedimiento no puede estar vacío.")

        elif not isinstance(categoria_equipo_requerida, str) or categoria_equipo_requerida == "":
            raise DatosInvalidosError("La categoría de equipo requerida no puede estar vacía.")

        elif not isinstance(certificaciones_requeridas, set) or not certificaciones_requeridas:
            raise DatosInvalidosError("Las certificaciones requeridas deben ser un conjunto no vacío.")
        elif not all(map(lambda cert: isinstance(cert, str) and cert != "", certificaciones_requeridas)):
            raise DatosInvalidosError("Cada certificación requerida debe ser un texto no vacío.")
        if type(limite_gravedad) is not int or limite_gravedad <= 0:
            raise DatosInvalidosError("El límite de gravedad debe ser un entero positivo")

        else:
            self.__ID = "PR" + str(Procedimiento.nextid)
            Procedimiento.nextid += 1
            self.__nombre = nombre 
            self.__categoria_equipo_requerida = categoria_equipo_requerida.lower() 
            self.__certificaciones_requeridas = certificaciones_requeridas
            self.__limite_gravedad = limite_gravedad

    def evaluar_unidad(self): 
        raise NotImplementedError ("No se está evaluando la unidad correctamente")


    def getter_limitegravedad(self):
        return self.__limite_gravedad

    def getter_nombre(self):
        return self.__nombre

    def getter_categoria_equipo(self):
        return self.__categoria_equipo_requerida

    def getter_certificaciones_requeridas(self):
        return self.__certificaciones_requeridas.copy()

    def getter_id(self):
        return self.__ID