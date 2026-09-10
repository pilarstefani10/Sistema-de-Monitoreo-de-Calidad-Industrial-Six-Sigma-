from Procedimiento import Procedimiento
class ProcedimientoVisual(Procedimiento):
    def __init__(self, nombre, categoria_equipo_requerida, certificacion_requerida, limite_gravedad, criterios, valor_esperado):
        super().__init__(nombre, categoria_equipo_requerida, certificacion_requerida, limite_gravedad)
        if not isinstance(criterios, list) or len(criterios) == 0:
            raise ValueError("Los criterios deben ser una lista no vacía.")
        #Criterios sería un diccionario con la estructura: {"criterio1": valor1, "criterio2": valor2, ...}