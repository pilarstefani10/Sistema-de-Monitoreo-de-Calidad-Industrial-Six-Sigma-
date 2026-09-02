 
from Muestra import Muestra


class Lote:

    def __init__(self, ID, cantidad_fabricada):

        if cantidad_fabricada <= 0:
            raise ValueError("La cantidad fabricada debe ser mayor a cero")

        if not isinstance(ID, int):
            raise ValueError("El ID del lote debe ser un número entero")


            
        self.ID = ID
        self.cantidad_fabricada = cantidad_fabricada
        self.estado = "PENDIENTE"
        self.muestras = []

    def crear_muestra(self, ID_muestra):
        cantidad_muestra = round(self.cantidad_fabricada * 0.05)
        muestra = Muestra(
            ID_muestra,
            cantidad_muestra,
            self)
        self.muestras.append(muestra)
        return muestra
    
