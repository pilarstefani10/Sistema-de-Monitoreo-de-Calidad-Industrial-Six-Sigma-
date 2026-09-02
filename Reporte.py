from datetime import date

class Reporte:

    def __init__(self, ID, fecha, muestra, lote, responsables, causas):

        self.ID = ID
        self.fecha = fecha
        self.muestra = muestra
        self.lote = lote
        self.responsables = responsables
        self.causas = causas
