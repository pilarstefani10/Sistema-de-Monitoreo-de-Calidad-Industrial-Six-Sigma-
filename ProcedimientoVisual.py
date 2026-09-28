from Procedimiento import Procedimiento
from Defecto import Defecto
import random
class ProcedimientoVisual(Procedimiento):
    def __init__(self, config_proc):
        super().__init__(config_proc.get("nombre"), config_proc.get("categoria_equipo_requerida"), config_proc.get("certificacion_requerida"), config_proc.get("limite_gravedad"))
        self.frases_posibles= config_proc.get("frases_posibles")

    def generar_kwargs(self):
        return {"zona_afectada": random.choice(self.config_proc.get("zonas_posibles")),
            "descripcion": random.choice(self.config_proc.get("descripciones")),
            "ocurrencia": random.choice(self.config_proc.get("ocurrencias"))}

    def evaluar_unidad(self,generar_kwargs):
        defecto = None
        # 1. Generamos la observación (1 = Anomalía, 0 = Conforme)
        """observacion = random.choices(
            [0, 1], 
            weights=[1 - self.probabilidad_defecto, self.probabilidad_defecto]
        )[0]"""
        observacion = generar_kwargs.get("ocurrencia")
        if observacion == 1:
            # random.choice() toma la lista y devuelve un único string al azar
            descripcion_al_azar = generar_kwargs.get("descripcion") + " en la zona " + generar_kwargs.get("zona_afectada")
            
            defecto = Defecto(
                tipo="Anomalía Visual del procedimiento " + self.nombre,
                descripcion=descripcion_al_azar,
                gravedad=5 
            )
        return defecto


