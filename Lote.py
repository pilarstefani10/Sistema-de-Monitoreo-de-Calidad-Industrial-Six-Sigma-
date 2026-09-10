 
from Muestra import Muestra
class Lote:
    nextid = 1
    def __init__(self, cantidad_fabricada):

        if not isinstance (cantidad_fabricada, int) or cantidad_fabricada <= 0:
            raise ValueError("La cantidad fabricada debe ser mayor a cero")
            
        self.ID = "L" + str(Lote.nextid)
        Lote.nextid += 1
        self.cantidad_fabricada = cantidad_fabricada
        self.estado = "PENDIENTE"
        self.muestras = []

    def crear_muestra(self):
        cantidad_muestra = round(self.cantidad_fabricada * 0.05)
        muestra = Muestra(
            str(self.ID) +"M" + str(len(self.muestras) + 1),
            cantidad_muestra,
            self)
        self.muestras.append(muestra)
        self.qmuestras+=1
        return muestra
    
