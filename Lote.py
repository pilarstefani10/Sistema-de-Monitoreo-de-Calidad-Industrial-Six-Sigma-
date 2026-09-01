 
class Lote:

    def __init__(self, id, cantidad_fabricada):

        if cantidad_fabricada <= 0:
            raise ValueError("La cantidad fabricada debe ser mayor a cero")

        self.id = id
        self.cantidad_fabricada = cantidad_fabricada
        self.estado = "PENDIENTE"
        self.muestras = []

    def agregar_muestra(self, muestra):
        muestra.lote = self
        self.muestras.append(muestra)