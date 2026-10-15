
import csv
from pathlib import Path
from Empresa import Empresa


class GestorArchivos:

    def __init__(self, empresa, carpeta="datos"):

        if not isinstance(empresa, Empresa):
            raise TypeError("Debe recibir una Empresa")

        self.__empresa = empresa
        self.__carpeta = Path(carpeta)

    def guardar(self):

        self.__carpeta.mkdir(
            parents=True,
            exist_ok=True
        )

        # Empresa entrega un diccionario con los
        # datos de todas las clases.
        datos = self.__empresa.exportar_datos()

        for nombre, informacion in datos.items():

            columnas = informacion["columnas"]
            filas = informacion["filas"]

            ruta = self.__carpeta / (nombre + ".csv")

            with open(
                ruta, "w",
                newline="",
                encoding="utf-8"
            ) as archivo:

                escritor = csv.DictWriter(
                    archivo,
                    fieldnames=columnas
                )

                escritor.writeheader()
                escritor.writerows(filas)

    def cargar(self):

        if not self.__carpeta.exists():
            return False

        # Empresa define qué archivos espera.
        estructura = self.__empresa.estructura_csv()
        datos = {}

        existentes = [
            (self.__carpeta / (nombre + ".csv")).exists()
            for nombre in estructura
        ]

        if not any(existentes):
            return False

        if not all(existentes):
            raise FileNotFoundError(
                "Faltan archivos del sistema"
            )

        for nombre, columnas in estructura.items():

            ruta = self.__carpeta / (nombre + ".csv")

            with open(
                ruta, "r",
                newline="",
                encoding="utf-8-sig"
            ) as archivo:

                lector = csv.DictReader(archivo)

                if lector.fieldnames != list(columnas):
                    raise ValueError(
                        "Columnas incorrectas en " + nombre
                    )

                datos[nombre] = list(lector)

        # Empresa reconstruye los objetos.
        self.__empresa.importar_datos(datos)

        return True


