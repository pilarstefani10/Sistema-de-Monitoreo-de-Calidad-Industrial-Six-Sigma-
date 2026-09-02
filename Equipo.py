from datetime import date

class Equipo:
    def __init__(self, ID, categoria, ultima_calibracion):

        if not isinstance(ultima_calibracion, date):
            raise ValueError("La ultima calibración debe ser un objeto de tipo date.")
        elif not ID.isdigit():
            raise ValueError("El ID del equipo debe ser un número entero.")
        
        else: 
            self.ultima_calibracion = ultima_calibracion
            self.ID = ID
            self.categoria = categoria




        

    
