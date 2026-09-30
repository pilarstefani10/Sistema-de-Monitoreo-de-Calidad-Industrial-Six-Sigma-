from Procedimiento import Procedimiento
from Defecto import Defecto
import random
class ProcedimientoVisual(Procedimiento):
    def __init__(self, **kwargs_config_proc):
        #Uso corchetes y no get para que falle si no encuentra algo con esa key
        super().__init__(kwargs_config_proc["nombre"]
                        , kwargs_config_proc["categoria_equipo_requerida"]
                        , kwargs_config_proc["certificacion_requerida"]
                        , kwargs_config_proc.get("limite_gravedad", 5))#Como para visual no hace falta el límite de gravedad
        
        self.descripciones= kwargs_config_proc["descripciones"]
        self.zonas_posibles = kwargs_config_proc["zonas_posibles"]
        self.probabilidad=kwargs_config_proc["probabilidad"]
    


    def generar_kwargs(self):
        return {"zona_afectada": random.choice(self.zonas_posibles),
            "descripcion": random.choice(self.descripciones),
            "ocurrencia":random.choices(
                [0, 1], 
                weights=[1 - self.probabilidad, self.probabilidad]
                )[0]}

    def evaluar_unidad(self):
        defecto = None
        # 1. Generamos la observación (1 = Anomalía, 0 = Conforme)
        Unidad=self.generar_kwargs()
        observacion = Unidad.get("ocurrencia")
        if observacion == 1:
            # random.choice() toma la lista y devuelve un único string al azar
            descripcion_al_azar = Unidad.get("descripcion") + " en la zona " + Unidad.get("zona_afectada")
            
            defecto = Defecto(
                tipo="Anomalía Visual del procedimiento " + self.getter_nombre(),
                descripcion=descripcion_al_azar,
                gravedad=5 
            )
        return defecto


