from Nodo import Nodo

class Pila:
    def __init__(self):
        self.__tope = None
        self.__tamanio = 0

    def esta_vacia(self):
        return self.__tope is None

    def __len__(self):
        return self.__tamanio

    def apilar(self, dato):
        nuevo = Nodo(dato)
        nuevo.setter_siguiente(self.__tope)
        self.__tope = nuevo
        self.__tamanio += 1

    def desapilar(self):
        if self.esta_vacia():
            return None

        dato = self.__tope.getter_dato()
        self.__tope = self.__tope.getter_siguiente()
        self.__tamanio -= 1
        return dato

    def tope(self):
        if self.esta_vacia():
            return None

        return self.__tope.getter_dato()

    def consultar_elementos(self):
        elementos = []
        actual = self.__tope

        while actual is not None:
            elementos.append(actual.getter_dato())
            actual = actual.getter_siguiente()

        return elementos