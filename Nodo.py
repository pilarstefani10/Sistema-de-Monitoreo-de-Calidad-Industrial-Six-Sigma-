class Nodo:
    def __init__(self, dato):
        self.__dato = dato
        self.__siguiente = None

    def getter_dato(self):
        return self.__dato

    def getter_siguiente(self):
        return self.__siguiente

    def setter_siguiente(self, siguiente):
        self.__siguiente = siguiente