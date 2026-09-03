class Defecto:
    def __init__(self, tipo, gravedad, descripcion):
        if not self.validar_tipo(tipo):
            raise ValueError("El nombre del defecto no puede estar vacío.")
        elif not isinstance(gravedad, int) or gravedad < 1 or gravedad > 5:
            raise ValueError("La gravedad del defecto debe ser un número entero entre 1 y 5.")
        elif not isinstance(descripcion, str) or descripcion == "":
            raise ValueError("La descripción del defecto no puede estar vacía.")
        else:
            self.tipo = tipo
            self.gravedad = gravedad
            self.descripcion = descripcion

    def es_critco(self):
        return self.gravedad == 5

    @staticmethod
    def validar_tipo(tipo):
            return isinstance(tipo, str) and tipo != ""

    def __str__(self):
        return f"Defecto: {self.tipo}, Gravedad: {self.gravedad}, Descripción: {self.descripcion}"

    def __repr__(self):
        return self.__str__()