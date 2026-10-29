from pathlib import Path
import csv


class GestorArchivos:

    @staticmethod
    def leer_csv_dict(ruta, encabezados=None):
        try:
            with open(ruta, "r", newline="", encoding="utf-8-sig") as archivo:
                lector = csv.DictReader(archivo)

                if lector.fieldnames is None:
                    raise ValueError("El CSV no tiene encabezados: " + ruta)

                if encabezados is not None:
                    if lector.fieldnames != list(encabezados):
                        raise ValueError("Encabezados incorrectos: " + ruta)

                return list(lector)

        except FileNotFoundError:
            return None

    @staticmethod
    def escribir_csv(ruta, encabezados, filas):
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(
                archivo,
                fieldnames=encabezados
            )

            escritor.writeheader()
            escritor.writerows(filas)

    @staticmethod
    def agregar_csv(ruta, encabezados, filas):
        # Abrimos en modo lectura para comprobar si
        # ya existe y si tiene encabezados.
        try:
            with open(ruta, "r", newline="", encoding="utf-8-sig") as archivo:
                lector = csv.reader(archivo)
                primera_fila = next(lector, None)

        except FileNotFoundError:
            primera_fila = None

        if primera_fila is not None:
            if primera_fila != list(encabezados):
                raise ValueError("Encabezados incorrectos: " + ruta)

        with open(ruta, "a", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(
                archivo,
                fieldnames=encabezados
            )

            if primera_fila is None:
                escritor.writeheader()

            escritor.writerows(filas)

    
    @staticmethod
    def guardar_reporte(nombre, contenido):
        carpeta = Path("datos/reportes")
        carpeta.mkdir(parents=True, exist_ok=True)

        ruta = carpeta / f"{nombre}.txt"

        try:
            with open(ruta, "x", encoding="utf-8") as archivo:
                archivo.write(contenido)

        except FileExistsError:
            with open(ruta, "r", encoding="utf-8") as archivo:
                if archivo.read() != contenido:
                    raise ValueError(
                        "Ya existe un reporte diferente con ese ID."
                    )

        return ruta
