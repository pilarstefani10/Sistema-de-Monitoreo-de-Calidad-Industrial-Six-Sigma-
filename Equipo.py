from datetime import date,timedelta
from Lista_Enlazada_Fechas_Calibracion import Lista_Calibraciones
class Equipo:
    nextid = 1

    def __init__(self, categoria, ultima_calibracion=None):

        if ultima_calibracion is not None and not isinstance(ultima_calibracion, date):
            raise ValueError("La ultima calibración debe ser un objeto de tipo date.")

        elif not isinstance(categoria, str) or categoria == "":
            raise ValueError("La categoria del equipo no puede estar vacía.")

        else: 
            self.__historial_calibraciones= Lista_Calibraciones()
            if ultima_calibracion is not None:
                self.__historial_calibraciones.agregar_ordenado(ultima_calibracion)

            self.__ID = "E" + str(Equipo.nextid)
            Equipo.nextid += 1
            self.__categoria = categoria.lower() 

    def calibrar(self, fecha):
        if not isinstance(fecha, date):
            raise ValueError("La fecha de calibración debe ser válida")

        if self.__historial_calibraciones.buscar(fecha):
            raise ValueError("La calibración ya está registrada")

        self.__historial_calibraciones.agregar_ordenado(fecha)

    
    def calibracion_vigente(self, fecha_inspeccion):
        ultima = self.getter_ultimacalibracion()

        if ultima is None:
            return False

        return (
            fecha_inspeccion - timedelta(days=182)
            <= ultima <= fecha_inspeccion
        )


    def eliminar_calibracion(self, fecha):
        return self.__historial_calibraciones.eliminar_buscando(fecha)

    def getter_ultimacalibracion(self):
        return self.__historial_calibraciones.obtener_ultimo()

    def getter_categoria(self):
        return self.__categoria

    def getter_id(self):
        return self.__ID

        

    
