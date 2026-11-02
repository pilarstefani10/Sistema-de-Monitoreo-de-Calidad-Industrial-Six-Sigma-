from NodoArbol import NodoArbol

class Arbol:
    def __init__(self):
        self.raiz = None
        self.tamanio = 0

    def es_vacio(self):
        return self.raiz is None

    def __len__(self):
        return self.tamanio

    def insertar(self, lote, nodo=None):
        if self.raiz is None:
            self.raiz = NodoArbol(lote)
            self.tamanio += 1
            return

        if nodo is None:
            nodo = self.raiz

        dato = int(lote.ID[1:])

        if dato < nodo.dato:
            if nodo.izquierda is None:
                nodo.izquierda = NodoArbol(lote)
                self.tamanio += 1
            else:
                self.insertar(lote, nodo.izquierda)

        elif dato > nodo.dato:
            if nodo.derecha is None:
                nodo.derecha = NodoArbol(lote)
                self.tamanio += 1
            else:
                self.insertar(lote, nodo.derecha)

        else:
            raise ValueError("El lote ya existe en el árbol")

    def buscar(self, nodo, dato):
        if nodo is None:
            return None

        if dato == nodo.dato:
            return nodo.lote

        if dato < nodo.dato:
            return self.buscar(nodo.izquierda, dato)

        return self.buscar(nodo.derecha, dato)

    def inorden(self, nodo):
        if nodo is None:
            return []

        return (
            self.inorden(nodo.izquierda)
            + [nodo.lote]
            + self.inorden(nodo.derecha)
        )

    def preorden(self, nodo):
        if nodo is None:
            return []

        return (
            [nodo.lote]
            + self.preorden(nodo.izquierda)
            + self.preorden(nodo.derecha)
        )

    def postorden(self, nodo):
        if nodo is None:
            return []

        return (
            self.postorden(nodo.izquierda)
            + self.postorden(nodo.derecha)
            + [nodo.lote]
        )

    def __str__(self):
        return str([lote.ID for lote in self.inorden(self.raiz)])