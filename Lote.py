 
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
        self.__cantidad_muestrada=0

    def crear_muestra(self,u):
       if self.getter_estado() == "PENDIENTE":
        if not isinstance(u,int) and u>0 and u<=(self.__cantidad_fabricada - self.__cantidad_muestrada):
                raise ValueError("No se puede crear una muestra con esa cantidad de unidades")
        else:
                cantidad_muestra = u
                self.__cantidad_muestrada+=u
                
                muestra = Muestra(
                    str(self.__ID) +"M" + str(len(self.__muestras) + 1),
                    cantidad_muestra,
                    self)

                self.__muestras.append(muestra)
                return muestra
       else:
           return None

    def decidir_estado(self):
        if self.muestras_cerradas():
            cantidad_no_conformes=sum(map(lambda muestra: 1 if muestra.getter_estado()=="RECHAZADA" else 0 ,self.__muestras))
            if cantidad_no_conformes/len(self.getter_muestras())>= 0.05:
                self.setter_estado("RECHAZADO")
            else:
                self.setter_estado("APROBADO")
        else:
            raise ValueError("Las muestras no han sido cerradas por completo")##########ERROR A PERSONALIZARRRRR
    
    
    def muestras_cerradas(self):
        return all(map(lambda muestra: True if muestra.getter_estado() != "EN_INSPECCION" else False, self.__muestras))

    def setter_estado(self, e):
        self.__estado=e

    def getter_estado(self):
        return self.__estado

    def getter_muestras(self):
        return self.__muestras.copy()

    def getter_id(self):
        return self.__ID