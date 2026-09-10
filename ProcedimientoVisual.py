from Procedimiento import Procedimiento
class ProcedimientoVisual(Procedimiento):
    def __init__(self, nombre, categoria_equipo_requerida, certificacion_requerida, limite_gravedad, valor_esperado, tolerancia):
        super().__init__(nombre, categoria_equipo_requerida, certificacion_requerida, limite_gravedad)
        self.valor_esperado = valor_esperado
        self.tolerancia = tolerancia

    def evaluar(self, observaciones):
        defectos = []

        minimo = self.valor_esperado - self.tolerancia
        maximo = self.valor_esperado + self.tolerancia

        for valor in observaciones:
            if valor < minimo or valor > maximo:
                # crear Defecto
                pass

        return defectos