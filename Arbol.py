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

        dato = int(lote.getter_id()[1:])

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

    def buscar(self, nodo, dato, pasos=0):
        if nodo is None:
            print(f"Búsqueda terminada en {pasos} pasos")
            return None

        pasos += 1

        if dato == nodo.dato:
            print(f"Lote encontrado en {pasos} pasos")
            return nodo.lote

        if dato < nodo.dato:
            return self.buscar(nodo.izquierda, dato,pasos)

        return self.buscar(nodo.derecha, dato,pasos)

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
        return str([lote.getter_id() for lote in self.inorden(self.raiz)])


    def _construir_balanceado(self, lotes, inicio, fin):
        if inicio > fin:
            return None

        medio = (inicio + fin) // 2

        nodo = NodoArbol(lotes[medio])

        nodo.izquierda = self._construir_balanceado(
            lotes, inicio, medio - 1
        )

        nodo.derecha = self._construir_balanceado(
            lotes, medio + 1, fin
        )

        return nodo

    def construir_balanceado(self, lotes):
        lotes_ordenados = sorted(
            lotes,
            key=lambda lote: int(lote.getter_id()[1:])
        )

        self.raiz = self._construir_balanceado(
            lotes_ordenados, 0, len(lotes_ordenados) - 1
        )
        self.tamanio = len(lotes_ordenados)