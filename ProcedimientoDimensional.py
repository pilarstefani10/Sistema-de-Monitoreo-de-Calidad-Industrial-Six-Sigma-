from Procedimiento import Procedimiento
from Defecto import Defecto
import random
class ProcedimientoDimensional(Procedimiento):
    def __init__(self, **kwargs_config_proc):
            self.validar_rangos_gravedad
            if not isinstance(kwargs_config_proc["limite_gravedad"], int) or kwargs_config_proc["limite_gravedad"] < 1:
                raise ValueError("El límite de gravedad debe ser un número entero mayor a 1.")
            elif not isinstance(kwargs_config_proc["valor_esperado"], float):
                raise ValueError("Los datos de creación del Procedimiento están incompletos o erróneos")
            elif not isinstance(kwargs_config_proc["tolerancia"], float):
                raise ValueError("")
            elif not isinstance(kwargs_config_proc["desvio"],float):
                raise ValueError("")
            
            super().__init__(kwargs_config_proc["nombre"],
                kwargs_config_proc["categoria_equipo_requerida"],
                kwargs_config_proc["certificacion_requerida"],
                kwargs_config_proc["limite_gravedad"])

            self.valor_esperado = kwargs_config_proc["valor_esperado"]
            self.tolerancia = kwargs_config_proc["tolerancia"]
            self.rangos_gravedad = kwargs_config_proc["rangos_gravedad"]  # Diccionario con los rangos de gravedad
            self.desvio= kwargs_config_proc["desvio"]
    
    def validar_rangos_gravedad(rangos):
        claves = ("leve", "moderado", "serio", "severo", "crítico")

        if not isinstance(rangos, dict):
            raise TypeError("rangos_gravedad debe ser un diccionario.")

        faltantes = [k for k in claves if k not in rangos]
        if faltantes:
            raise ValueError(f"Faltan rangos de gravedad: {faltantes}")

        for k in claves:
            if not isinstance(rangos[k], (int, float)):
                raise TypeError(f"El rango '{k}' debe ser numérico.")

        if not (rangos["leve"] < rangos["moderado"] < rangos["serio"] < rangos["severo"]):
            raise ValueError(
                "Los rangos deben estar en orden creciente: leve < moderado < serio < severo."
            )
    
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
        return defecto



    


