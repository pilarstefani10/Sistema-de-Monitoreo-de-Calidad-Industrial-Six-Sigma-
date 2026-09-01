class Defecto:
    def __init__(self, nombre, gravedad):
        if not self.validar_nombre(nombre):
            raise ValueError("El nombre del defecto no puede estar vacío.")
        if not isinstance(gravedad, int) or gravedad < 1 or gravedad > 5:
            raise ValueError("La gravedad del defecto debe ser un número entero entre 1 y 5.")
        self.nombre = nombre
        self.gravedad = gravedad

    def es_critco(self):
        return self.gravedad == 5

    @staticmethod
    def validar_nombre(nombre):
            return isinstance(nombre, str) and nombre != ""

