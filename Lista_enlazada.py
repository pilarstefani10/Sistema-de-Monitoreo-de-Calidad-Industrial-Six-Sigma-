from Nodo import Nodo
class Lista:
    def __init__(self):
        self.__cabeza = None
        self.__tamanio = 0

    def getter_cabeza(self):
        return self.__cabeza

    def setter_cabeza(self, nodo):
        self.__cabeza = nodo

    def aumentar_tamanio(self):
        self.__tamanio += 1

    def disminuir_tamanio(self):
        self.__tamanio -= 1

    def es_vacia(self):
        return self.__cabeza is None

    def __len__(self):
        return self.__tamanio

    def agregar_inicio(self, dato):
        nuevo_nodo = Nodo(dato)
        nuevo_nodo.setter_siguiente(self.__cabeza)
        self.__cabeza = nuevo_nodo
        self.aumentar_tamanio()

    def agregar_final(self, dato):
        nuevo_nodo = Nodo(dato)

        if self.es_vacia():
            self.__cabeza = nuevo_nodo
        else:
            actual = self.__cabeza

            while actual.getter_siguiente() is not None:
                actual = actual.getter_siguiente()

            actual.setter_siguiente(nuevo_nodo)

        self.aumentar_tamanio()

    def __str__(self):
        cadena = ""
        actual = self.__cabeza

        while actual is not None:
            cadena += str(actual.getter_dato()) + " -> "
            actual = actual.getter_siguiente()

        return cadena

    def buscar(self, dato):
        actual = self.__cabeza

        while actual is not None:
            if actual.getter_dato() == dato:
                return True

            actual = actual.getter_siguiente()

        return False

    def eliminar_buscando(self, dato):
        if not self.buscar(dato):
            return False

        actual = self.__cabeza
        anterior = None

        while actual is not None:
            if actual.getter_dato() == dato:

                if anterior is None:
                    self.__cabeza = actual.getter_siguiente()
                else:
                    anterior.setter_siguiente(actual.getter_siguiente())

                self.disminuir_tamanio()
                return True

            anterior = actual
            actual = actual.getter_siguiente()

        return False