from Lista_enlazada import Lista
from Nodo import Nodo


class Lista_Calibraciones(Lista):

    def __init__(self):
        super().__init__()
        self.__ultimo = None

    def getter_ultimo(self):
        return self.__ultimo

    def setter_ultimo(self, nodo):
        self.__ultimo = nodo

    def agregar_ordenado(self, dato):
        nuevo_nodo = Nodo(dato)

        if self.es_vacia():
            self.setter_cabeza(nuevo_nodo)
            self.setter_ultimo(nuevo_nodo)

        elif dato < self.getter_cabeza().getter_dato():
            nuevo_nodo.setter_siguiente(self.getter_cabeza())
            self.setter_cabeza(nuevo_nodo)

        else:
            actual = self.getter_cabeza()

            while (actual.getter_siguiente() is not None
                   and actual.getter_siguiente().getter_dato() <= dato):
                actual = actual.getter_siguiente()

            nuevo_nodo.setter_siguiente(actual.getter_siguiente())
            actual.setter_siguiente(nuevo_nodo)

            if nuevo_nodo.getter_siguiente() is None:
                self.setter_ultimo(nuevo_nodo)

        self.aumentar_tamanio()

    def obtener_ultimo(self):
        if self.getter_ultimo() is None:
            return None

        return self.getter_ultimo().getter_dato()

    def eliminar_buscando(self, dato):
        if self.es_vacia():
            return False

        actual = self.getter_cabeza()
        anterior = None

        while actual is not None:
            if actual.getter_dato() == dato:

                if anterior is None:
                    self.setter_cabeza(actual.getter_siguiente())
                else:
                    anterior.setter_siguiente(actual.getter_siguiente())

                if actual == self.getter_ultimo():
                    self.setter_ultimo(anterior)

                self.disminuir_tamanio()
                return True

            anterior = actual
            actual = actual.getter_siguiente()

        return False

    def agregar_inicio(self, dato):
        self.agregar_ordenado(dato)

    def agregar_final(self, dato):
        self.agregar_ordenado(dato)