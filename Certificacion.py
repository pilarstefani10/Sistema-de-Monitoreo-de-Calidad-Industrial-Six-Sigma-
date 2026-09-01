from datetime import date
class Certificacion:
    def __init__(self, name, fecha_inicio, fecha_vencimiento):
        if not self.validar_nombre(name):
            raise ValueError("El nombre de la certificación no puede estar vacío.")
        elif not self.validar_fechas(fecha_inicio, fecha_vencimiento):
            raise ValueError("Las fechas de inicio y vencimiento no son válidas.")
        else:
            self.name = name
            self.fecha_inicio = fecha_inicio
            self.fecha_vencimiento = fecha_vencimiento

    @staticmethod
    def validar_nombre(nombre):
        return isinstance(nombre, str) and nombre != ""

    @staticmethod
    def validar_fechas(fecha_inicio, fecha_vencimiento):
        return (
            isinstance(fecha_inicio, date)
            and isinstance(fecha_vencimiento, date)
            and fecha_inicio <= fecha_vencimiento
        )

    def esta_vigente(self, fecha):
        return self.fecha_inicio <= fecha <= self.fecha_vencimiento