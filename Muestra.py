
class Muestra:

    def __init__(self, ID, unidades_representadas, lote):

        if unidades_representadas <= 0:
            raise ValueError(
                "Las unidades representadas deben ser mayores a cero"
            )

        self.ID = ID
        self.unidades_representadas = unidades_representadas

        self.estado = "PENDIENTE"
        self.lote = lote
        self.defectos = []
        self.inspeccion = None

    def iniciar_inspeccion(self):

        if self.estado != "PENDIENTE":
            raise ValueError(
                "Solo se puede inspeccionar una muestra pendiente"
            )

        self.estado = "EN_INSPECCION"