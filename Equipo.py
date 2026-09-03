from datetime import date

class Equipo:
    nextid = 1
    def __init__(self, categoria, ultima_calibracion):

        if not isinstance(ultima_calibracion, date):
            raise ValueError("La ultima calibración debe ser un objeto de tipo date.")

        elif not isinstance(categoria, str) or categoria == "":
            raise ValueError("La categoria del equipo no puede estar vacía.")

        else: 
            self.ultima_calibracion = ultima_calibracion
            self.ID = "E" + str(self.nextid)
            self.nextid += 1
            self.categoria = categoria.lower() 

    def calibrar(self, fecha_calibracion):
        if not isinstance(fecha_calibracion, date):
            raise ValueError("La fecha de calibración debe ser un objeto de tipo date.")
        elif fecha_calibracion < self.ultima_calibracion:
            raise ValueError("La nueva fecha de calibración no puede ser anterior a la última calibración.")
        else:
            self.ultima_calibracion = fecha_calibracion


        

    
