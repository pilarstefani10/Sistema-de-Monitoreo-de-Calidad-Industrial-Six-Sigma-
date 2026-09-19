from Procedimiento import Procedimiento
class ProcedimientoDimensional(Procedimiento):
    def __init__(self, nombre, categoria_equipo_requerida, certificacion_requerida, limite_gravedad, valor_esperado, tolerancia, rangos_gravedad):
            super().__init__(nombre, categoria_equipo_requerida, certificacion_requerida, limite_gravedad)
            self.valor_esperado = valor_esperado
            self.tolerancia = tolerancia
            self.rangos_gravedad = rangos_gravedad  # Diccionario con los rangos de gravedad
    
    def calcular_gravedad(self,diferencia):
        if diferencia < self.rangos_gravedad["leve"]:
            return 1
        elif diferencia < self.rangos_gravedad["moderado"]:
            return 2
        elif diferencia < self.rangos_gravedad["serio"]:
            return 3
        elif diferencia < self.rangos_gravedad["severo"]:
            return 4
        else:
            return 5

    def evaluar(self, observaciones):
        defectos = []
    
        for valor in observaciones:

            diferencia = abs(valor - self.valor_esperado)

            if diferencia > self.tolerancia:

                gravedad = self.calcular_gravedad(diferencia)
    
            return defectos
        #Criterios sería un diccionario con la estructura: {"criterio1": valor1, "criterio2": valor2, ...}