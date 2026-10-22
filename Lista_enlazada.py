from Nodo import Nodo
class Lista:
    def __init__(self):
        self.cabeza = None
        self.tamanio = 0

    def es_vacia(self):
        return self.cabeza is None

    def __len__(self):
        return self.tamanio

    def agregar_inicio(self, dato):
        nuevo_nodo = Nodo(dato)
        nuevo_nodo.siguiente = self.cabeza
        self.cabeza = nuevo_nodo
        self.tamanio += 1

    def agregar_final(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.es_vacia():
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self.tamanio += 1

    def __str__(self):
        cadena = ""
        actual = self.cabeza
        while actual is not None:
            cadena += str(actual) + " -> "
            actual = actual.siguiente
        return cadena

    def buscar(self, dato):
        actual = self.cabeza
        while actual is not None:
            if actual.dato == dato:
                return True
            actual = actual.siguiente
        return False

    def eliminar_buscando(self, dato):
        if not self.buscar(dato):
            return False

        actual = self.cabeza
        anterior = None

        while actual is not None:
            if actual.dato == dato:
                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                self.tamanio -= 1
                return True
            anterior = actual
            actual = actual.siguiente

        return False
