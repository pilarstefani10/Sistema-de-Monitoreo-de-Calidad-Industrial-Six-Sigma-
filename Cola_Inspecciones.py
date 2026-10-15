from Nodo import Nodo

class Cola:
    def __init__(self):
        self.__inicio = None
        self.__final = None

    def esta_vacia(self):
        return self.__inicio is None

    def encolar(self, dato):
        nuevo = Nodo(dato)

        if self.esta_vacia():
            self.__inicio = nuevo
            self.__final = nuevo

        else:
            self.__final.setter_siguiente(nuevo)
            self.__final = nuevo

    def desencolar(self):
        if self.esta_vacia():
            raise ValueError("La cola está vacía")

        dato = self.__inicio.getter_dato()

        self.__inicio = self.__inicio.getter_siguiente()

        if self.__inicio is None:
            self.__final = None

        return dato

    def frente(self):
        if self.esta_vacia():
            return None

        return self.__inicio.getter_dato()

    def consultar_elementos(self):
        elementos = []
        actual = self.__inicio

        while actual is not None:
            elementos.append(actual.getter_dato())
            actual = actual.getter_siguiente()

        return elementos