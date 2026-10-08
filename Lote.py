 
from Muestra import Muestra

class Lote:
    nextid = 1

    def __init__(self, cantidad_fabricada):

        if not isinstance (cantidad_fabricada, int) or cantidad_fabricada <= 0:
            raise ValueError("La cantidad fabricada debe ser mayor a cero")
            
        self.__ID = "L" + str(Lote.nextid)
        Lote.nextid += 1
        
        self.__cantidad_fabricada = cantidad_fabricada
        self.__estado = "PENDIENTE"
        self.__muestras = []

    def crear_muestra(self, fecha, profesional, equipo, procedimiento):
        cantidad_muestra = round(self.__cantidad_fabricada * 0.05)

        if not self.puede_agregar_muestra(cantidad_muestra):
            raise ValueError("La muestra supera la cantidad disponible del lote.")
        
        muestra = Muestra(
            str(self.__ID) +"M" + str(len(self.__muestras) + 1),
            cantidad_muestra,
            self)

        #muestra.crear_inspeccion(fecha, profesional, equipo, procedimiento)
        
        self.__muestras.append(muestra)
        return muestra

    def puede_agregar_muestra(self, cantidad_muestra):
        total = sum(map(lambda muestra: muestra.getter_unidadesrepresentadas(),self.__muestras))
        return total + cantidad_muestra <= self.__cantidad_fabricada

    def getter_estado(self):
        return self.__estado

    def getter_muestras(self):
        return self.__muestras.copy()

    def getter_id(self):
        return self.__ID