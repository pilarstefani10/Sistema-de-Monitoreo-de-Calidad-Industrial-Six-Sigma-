
class Procedimiento:

    def __init__(self, ID, nombre, categoria_equipo_requerida, certificacion_requerida, limite_gravedad):
        if not ID.isdigit():
            raise ValueError("El ID del procedimiento debe ser un número entero.")

        elif not isinstance(nombre, str) or nombre == "":
            raise ValueError("El nombre del procedimiento no puede estar vacío.")

        elif not isinstance(categoria_equipo_requerida, str) or categoria_equipo_requerida == "":
            raise ValueError("La categoría de equipo requerida no puede estar vacía.")

        elif not isinstance(certificacion_requerida, str) or certificacion_requerida == "":
            raise ValueError("La certificación requerida no puede estar vacía.")

        elif not isinstance(limite_gravedad, int) or limite_gravedad < 1 or limite_gravedad > 5:
            raise ValueError("El límite de gravedad debe ser un número entero entre 1 y 5.")

        else:
            self.ID = ID
            self.nombre = nombre 
            self.categoria_equipo_requerida = categoria_equipo_requerida
            self.certificacion_requerida = certificacion_requerida
            self.limite_gravedad = limite_gravedad
        
