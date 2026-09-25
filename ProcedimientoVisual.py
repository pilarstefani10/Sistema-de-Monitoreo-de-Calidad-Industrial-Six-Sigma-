from Procedimiento import Procedimiento
from Defecto import Defecto
import random
class ProcedimientoVisual(Procedimiento):
    def __init__(self, nombre, categoria_equipo_requerida, certificacion_requerida, limite_gravedad,frases_posibles):
        super().__init__(nombre, categoria_equipo_requerida, certificacion_requerida, limite_gravedad)
        self.frases_posibles= frases_posibles

    def evaluar_unidad(self):
        defecto = None
        # 1. Generamos la observación (1 = Anomalía, 0 = Conforme)
        # 1 tiene una probabilidad muy baja (ej: 5%)
        observacion = random.choices(
            [0, 1], 
            weights=[1 - self.probabilidad_defecto, self.probabilidad_defecto]
        )[0]
        if observacion == 1:
            # random.choice() toma la lista y devuelve un único string al azar
            descripcion_al_azar = random.choice(self.frases_posibles)
            
            defecto = Defecto(
                tipo="Anomalía Visual del procedimiento " + self.nombre,
                descripcion=descripcion_al_azar,
                gravedad=5 
            )
        return defecto, descripcion_al_azar


