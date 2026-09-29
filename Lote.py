 
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

    def crear_muestra(self, fecha, profesional, equipo, procedimiento):
        cantidad_muestra = round(self.cantidad_fabricada * 0.05)

        if not self.puede_agregar_muestra(cantidad_muestra):
            raise ValueError("La muestra supera la cantidad disponible del lote.")
        
        muestra = Muestra(
            str(self.ID) +"M" + str(len(self.muestras) + 1),
            cantidad_muestra,
            self)

        muestra.crear_inspeccion(fecha, profesional, equipo, procedimiento)
        
        self.muestras.append(muestra)
        return muestra

    def puede_agregar_muestra(self, cantidad_muestra):

        total = 0

        for muestra in self.muestras:
            total += muestra.getter_unidadesrepresentadas()

        return total + cantidad_muestra <= self.cantidad_fabricada
    
