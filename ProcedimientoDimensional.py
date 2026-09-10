from Procedimiento import Procedimiento
class ProcedimientoDimensional(Procedimiento):
    def __init__(self, nombre, categoria_equipo_requerida, certificacion_requerida, limite_gravedad, valor_esperado, tolerancia):
            super().__init__(nombre, categoria_equipo_requerida, certificacion_requerida, limite_gravedad)
            self.valor_esperado = valor_esperado
            self.tolerancia = tolerancia
    
    def evaluar(self, observaciones):
        defectos = []
    
        minimo = self.valor_esperado - self.tolerancia
        maximo = self.valor_esperado + self.tolerancia

        cumple= lambda valor: minimo <= valor <= maximo
        for valor in observaciones:
            if valor < minimo or valor > maximo:
                    # crear Defecto
                pass
    
            return defectos
        #Criterios sería un diccionario con la estructura: {"criterio1": valor1, "criterio2": valor2, ...}