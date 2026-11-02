class NodoArbol:
    def __init__(self, lote):
        self.lote = lote
        self.dato = int(lote.getter_ID()[1:])
        self.izquierda = None
        self.derecha = None