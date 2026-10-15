
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
