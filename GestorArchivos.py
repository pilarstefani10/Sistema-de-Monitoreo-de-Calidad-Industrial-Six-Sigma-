class GestorDeArchivos:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo

    def leer_archivo(self):
        try:
            with open(self.nombre_archivo, 'r') as archivo:
                contenido = archivo.read()
                return contenido
        except FileNotFoundError:
            print(f"El archivo {self.nombre_archivo} no se encontró.")
            return None

    def escribir_archivo(self, contenido):
        try:
            with open(self.nombre_archivo, 'w') as archivo:
                archivo.write(contenido)
                print(f"Contenido escrito en {self.nombre_archivo}.")
        except Exception as e:
            print(f"Ocurrió un error al escribir en el archivo: {e}")

    def agregar_a_archivo(self, contenido):
        try:
            with open(self.nombre_archivo, 'a') as archivo:
                archivo.write(contenido)
                print(f"Contenido agregado a {self.nombre_archivo}.")
        except Exception as e:
            print(f"Ocurrió un error al agregar al archivo: {e}") 





        pro       ,def       , lote       ,    certi