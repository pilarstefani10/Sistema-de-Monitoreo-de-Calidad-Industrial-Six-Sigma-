
class Procedimiento:
    nextid = 1
    def __init__(self, nombre, categoria_equipo_requerida, certificacion_requerida, limite_gravedad):
        if not isinstance(nombre, str) or nombre == "":
            raise ValueError("El nombre del procedimiento no puede estar vacío.")

        elif not isinstance(categoria_equipo_requerida, str) or categoria_equipo_requerida == "":
            raise ValueError("La categoría de equipo requerida no puede estar vacía.")

        elif not isinstance(certificacion_requerida, str) or certificacion_requerida == "":
            raise ValueError("La certificación requerida no puede estar vacía.")

        else:
            self.ID = "PR" + str(Procedimiento.nextid)
            Procedimiento.nextid += 1
            self.nombre = nombre 
            self.categoria_equipo_requerida = categoria_equipo_requerida.lower() 
            self.certificacion_requerida = certificacion_requerida
            self.limite_gravedad = limite_gravedad

    def evaluar_unidad(self): 
        raise NotImplementedError ("No se está evaluando la unidad correctamente")


    def getter_limitegravedad(self):
        return self.limite_gravedad
        
