class Defecto:
    def __init__(self, tipo, gravedad, descripcion):
        if not self.validar_tipo(tipo):
            raise ValueError("El nombre del defecto no puede estar vacío.")
        elif not isinstance(gravedad, int) or gravedad < 1 or gravedad > 5:
            raise ValueError("La gravedad del defecto debe ser un número entero entre 1 y 5.")
        elif not isinstance(descripcion, str) or descripcion == "":
            raise ValueError("La descripción del defecto no puede estar vacía.")
        else:
            self.__tipo = tipo
            self.__gravedad = gravedad
            self.__descripcion = descripcion

    def es_critico(self):
        return self.__gravedad == 5

    @staticmethod
    def validar_tipo(tipo):
            return isinstance(tipo, str) and tipo != ""

    def getter_gravedad(self):
        return self.__gravedad

    def getter_descripcion(self):
        return self.__descripcion
    
    def __str__(self):
        return f"Defecto: {self.__tipo}, Gravedad: {self.__gravedad}, Descripción: {self.__descripcion}"

    def __repr__(self):
        return self.__str__()

    def getter_tipo(self):
        return self.__tipo