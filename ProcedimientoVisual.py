from Procedimiento import Procedimiento
from Defecto import Defecto
from Excepciones import DatosInvalidosError
import random,json
class ProcedimientoVisual(Procedimiento):
    def __init__(self, **kwargs_config_proc):
        #Uso corchetes y no get para que falle si no encuentra algo con esa key
        if not isinstance(kwargs_config_proc["probabilidad"], float) or not (0<kwargs_config_proc["probabilidad"]<1):
            raise DatosInvalidosError ("La probabilidad de ocurrencia de un Defecto Visual debe ser un numero entre 0 y 1")
        if not ProcedimientoVisual.lista_de_textos_valida(kwargs_config_proc["zonas_posibles"]):
            raise DatosInvalidosError("Las zonas posibles deben ser una lista de textos no vacía")
        if not ProcedimientoVisual.lista_de_textos_valida(kwargs_config_proc["descripciones"]):
            raise DatosInvalidosError("Las descripciones deben ser una lista de textos no vacía")
        super().__init__(kwargs_config_proc["nombre"]
                        , kwargs_config_proc["categoria_equipo_requerida"]
                        , kwargs_config_proc["certificaciones_requeridas"]
                        , kwargs_config_proc.get("limite_gravedad", 5))#Como para visual no hace falta el límite de gravedad
        
        self.__descripciones= kwargs_config_proc["descripciones"]
        self.__zonas_posibles = kwargs_config_proc["zonas_posibles"]
        self.__probabilidad=kwargs_config_proc["probabilidad"]
    
    @staticmethod
    def lista_de_textos_valida(lista):
        return isinstance(lista, list) and len(lista) > 0 and all(map(lambda texto: isinstance(texto, str) and texto != "", lista))

    def generar_kwargs(self):
        return {"zona_afectada": random.choice(self.__zonas_posibles),
            "descripcion": random.choice(self.__descripciones),
            "ocurrencia":random.choices(
                [0, 1], 
                weights=[1 - self.__probabilidad, self.__probabilidad]
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

    def estandarizar(self):
        datos = super().estandarizar()

        datos.update({
            "tipo": "visual",
            "probabilidad": self.__probabilidad,
            "zonas_posibles": json.dumps(
                self.__zonas_posibles,
                ensure_ascii=False
            ),
            "descripciones": json.dumps(
                self.__descripciones,
                ensure_ascii=False
            )
        })

        return datos

    def getter_probabilidad(self):
        return self.__probabilidad

    def getter_zonas_posibles(self):
        return self.__zonas_posibles.copy()

    def getter_descripciones(self):
        return self.__descripciones.copy()
