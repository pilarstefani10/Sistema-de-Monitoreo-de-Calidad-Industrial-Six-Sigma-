
from Lista_enlazada import Lista
from Nodo import Nodo

class Lista_Calibraciones(Lista):

    def __init__(self):
        super().__init__()
        self.ultimo = None

    def agregar_ordenado(self, dato):
        nuevo_nodo = Nodo(dato)

        if self.es_vacia():
            self.cabeza = nuevo_nodo
            self.ultimo = nuevo_nodo


        elif dato < self.cabeza.getter_dato():
            nuevo_nodo.setter_siguiente(self.cabeza)
            self.cabeza = nuevo_nodo

        else:
            actual = self.cabeza


            while (actual.getter_siguiente() is not None
                    and actual.getter_siguiente().getter_dato() <= dato):
                actual = actual.getter_siguiente()

            nuevo_nodo.setter_siguiente(actual.getter_siguiente())
            actual.setter_siguiente(nuevo_nodo)






            if nuevo_nodo.siguiente is None:
                self.ultimo = nuevo_nodo

        self.tamanio += 1

    def obtener_ultimo(self):
        if self.ultimo is None:
            return None

        return self.ultimo.dato

    def eliminar_buscando(self, dato):
        if self.es_vacia():
            return False

        actual = self.cabeza
        anterior = None

        while actual is not None:
            if actual.dato == dato:

                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente

                if actual == self.ultimo:
                    self.ultimo = anterior

                self.tamanio -= 1
                return True

            anterior = actual
            actual = actual.siguiente

        return False

    def agregar_inicio(self, dato):
        self.agregar_ordenado(dato)

    def agregar_final(self, dato):
        self.agregar_ordenado(dato)
