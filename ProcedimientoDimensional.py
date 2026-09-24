from Procedimiento import Procedimiento
from Defecto import Defecto
import random
class ProcedimientoDimensional(Procedimiento):
    def __init__(self, nombre, categoria_equipo_requerida, certificacion_requerida, limite_gravedad, valor_esperado, tolerancia, rangos_gravedad,desvio):
            super().__init__(nombre, categoria_equipo_requerida, certificacion_requerida, limite_gravedad)
            self.valor_esperado = valor_esperado
            self.tolerancia = tolerancia
            self.rangos_gravedad = rangos_gravedad  # Diccionario con los rangos de gravedad
            self.desvio_estandar= desvio
    
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

    def evaluar_unidad(self):
        defecto =  None
        gravedad = 0
        observacion = random.gauss(self.valor_esperado, self.desvio)
        diferencia = abs(observacion - self.valor_esperado)
        if diferencia > self.tolerancia:
            gravedad = self.calcular_gravedad(diferencia)
            defecto = Defecto(
                    tipo="Desviación Dimensional",
                    descripcion=f"Medida {observacion:.4f} excedió la tolerancia por {diferencia:.4f}",
                    gravedad=gravedad
                )
        return defecto, gravedad
        #Criterios sería un diccionario con la estructura: {"criterio1": valor1, "criterio2": valor2, ...}




