from Certificacion import Certificacion
from Empleado import Empleado
from Cola_Inspecciones import Cola

class Profesional(Empleado):
    nextid = 1
    
    def __init__(self, name):
        super().__init__(name, "P" + str(Profesional.nextid))
        Profesional.nextid += 1
        self.__certificaciones = []
        self.__cola_inspecciones=Cola()

    def agregar_certificacion(self, nombre, fecha_inicio, fecha_vencimiento):
        certificacion = Certificacion(nombre, fecha_inicio, fecha_vencimiento)
        self.__certificaciones.append(certificacion)
        return certificacion

    def certificacion_vigente(self, nombre_certificacion, fecha):
        return any(map(lambda cert: cert.getter_nombre() == nombre_certificacion and cert.esta_vigente(fecha),self.__certificaciones))
        

    def __str__(self):
        return f"Profesional: {self.getter_nombre()}, ID: {self.getter_id()}, Certificaciones: {[cert.getter_nombre() for cert in self.__certificaciones]}"  
    

    def asignar_inspeccion(self, inspeccion):
        if inspeccion.getter_profesional() is not self:
            raise ValueError(
                "La inspección pertenece a otro profesional"
            )

        if inspeccion in self.getter_inspecciones_pendientes():
            raise ValueError(
                "La inspección ya está asignada"
            )

        if inspeccion.getter_muestra().getter_estado() != "PENDIENTE":
            raise ValueError(
                "La muestra no está pendiente"
            )

        self.__cola_inspecciones.encolar(inspeccion)

    def siguiente_inspeccion(self):
        return self.__cola_inspecciones.frente()

    def ejecutar_siguiente_inspeccion(self):

        inspeccion = self.__cola_inspecciones.frente()

        if inspeccion is None:
            raise ValueError("No hay inspecciones pendientes")############ERROR A PERSONALIZARRRRRR

        inspeccion.ejecutar()

        self.__cola_inspecciones.desencolar()

        return inspeccion

    def calibrar_equipo(self, equipo, fecha):
        equipo.calibrar(fecha)

    def getter_certificaciones(self):
        return self.__certificaciones.copy()

    def getter_inspeccion_pendiente(self):
        return self.__cola_inspecciones.frente()

    def getter_inspecciones_pendientes(self):
        return self.__cola_inspecciones.consultar_elementos()

    def getter_cola_vacia(self):
        return self.__cola_inspecciones.esta_vacia()