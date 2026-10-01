from datetime import date

class Equipo:
    nextid = 1

    def __init__(self, categoria, ultima_calibracion):

        if not isinstance(ultima_calibracion, date):
            raise ValueError("La ultima calibración debe ser un objeto de tipo date.")

        elif not isinstance(categoria, str) or categoria == "":
            raise ValueError("La categoria del equipo no puede estar vacía.")

        else: 
            self.__ultima_calibracion = ultima_calibracion
            self.__ID = "E" + str(Equipo.nextid)
            Equipo.nextid += 1
            self.__categoria = categoria.lower() 

    def calibrar(self, fecha_calibracion):
        if not isinstance(fecha_calibracion, date):
            raise ValueError("La fecha de calibración debe ser un objeto de tipo date.")
        elif fecha_calibracion < self.__ultima_calibracion:
            raise ValueError("La nueva fecha de calibración no puede ser anterior a la última calibración.")
        else:
            self.__ultima_calibracion = fecha_calibracion

    def getter_ultima_calibracion(self):
        return self.__ultima_calibracion

    def getter_categoria(self):
        return self.__categoria

    def getter_id(self):
        return self.__ID

        

    
