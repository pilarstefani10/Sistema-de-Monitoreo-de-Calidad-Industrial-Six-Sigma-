class Empleado:

    def __init__(self, name, ID):
        if not isinstance(name, str) or name == "":
            raise ValueError("El nombre del empleado no puede estar vacío.")

        self.__name = name
        self.__ID = ID

    def getter_nombre(self):
        return self.__name

    def getter_id(self):
        return self.__ID