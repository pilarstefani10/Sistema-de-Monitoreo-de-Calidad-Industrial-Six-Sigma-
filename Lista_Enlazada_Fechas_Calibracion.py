from Lista_enlazada import Lista
from Nodo import Nodo
class Lista_Calibraciones(Lista):
    def __init__(self):
        super().__init__()
        self.ultimo=None

    def es_vacia(self):
        return super().es_vacia()  and self.ultimo==None
    
    def agregar_ordenado(self, dato):
        nuevo_nodo = Nodo(dato)

        if self.es_vacia() or dato < self.cabeza.dato:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza = nuevo_nodo

        else:
            actual = self.cabeza

            while actual.siguiente is not None and actual.siguiente.dato <= dato:
                actual = actual.siguiente

            nuevo_nodo.siguiente = actual.siguiente
            actual.siguiente = nuevo_nodo

        self.tamanio += 1

    def obtener_ultimo(self):
        if self.es_vacia():
            return None

        actual = self.cabeza

        while actual.siguiente is not None:
            actual = actual.siguiente

        return actual.dato

    def agregar_inicio(self, dato):
        self.agregar_ordenado(dato)

    def agregar_final(self, dato):
        self.agregar_ordenado(dato)