 
from Muestra import Muestra
from ProcedimientoDimensional import ProcedimientoDimensional
from Excepciones import DatosInvalidosError, TransicionInvalidaError

class Lote:
    nextid = 1

    def __init__(self, cantidad_fabricada):

        if not isinstance (cantidad_fabricada, int) or cantidad_fabricada <= 0:
            raise DatosInvalidosError("La cantidad fabricada debe ser mayor a cero")
            
        self.__ID = "L" + str(Lote.nextid)
        Lote.nextid += 1
        
        self.__cantidad_fabricada = cantidad_fabricada
        self.__estado = "PENDIENTE"
        self.__muestras = []
        self.__cantidad_muestrada=0

    def proximo_id_muestra(self):
        return self.__ID + "M" + str(len(self.__muestras) + 1)

    def validar_extraccion(self, unidades):
        disponibles = self.__cantidad_fabricada - self.__cantidad_muestrada

        if self.__estado != "PENDIENTE":
            raise TransicionInvalidaError("El lote " + self.__ID + " ya fue evaluado: no se le pueden extraer muestras.")
        if not isinstance(unidades, int) or unidades <= 0:
            raise DatosInvalidosError("Las unidades de la muestra deben ser un entero mayor a cero.")
        if unidades > disponibles:
            raise DatosInvalidosError("El lote " + self.__ID + " solo tiene " + str(disponibles) + " unidades disponibles.")

    def agregar_muestra(self, muestra):
        self.validar_extraccion(muestra.getter_unidadesrepresentadas())

        if muestra.getter_lote() is not self:
            raise DatosInvalidosError("La muestra pertenece a otro lote.")
        if muestra in self.__muestras:
            raise DatosInvalidosError("La muestra ya está en el lote.")

        self.__cantidad_muestrada += muestra.getter_unidadesrepresentadas()
        self.__muestras.append(muestra)


    def resultado_segun_criterio(self):
        if not self.__muestras:
            raise TransicionInvalidaError("El lote " + self.__ID + " no tiene muestras.")
        if not self.muestras_cerradas():
            raise TransicionInvalidaError("El lote " + self.__ID + " tiene muestras sin inspeccionar.")

        no_conformes = len(list(filter(lambda muestra: muestra.getter_estado() == "NO_CONFORME", self.__muestras)))

        if no_conformes / len(self.__muestras) > 0.05:
            return "RECHAZADO"
        return "APROBADO"

    def registrar_resultado(self, resultado):
        if self.__estado != "PENDIENTE":
            raise TransicionInvalidaError("El lote " + self.__ID + " ya fue evaluado.")
        if resultado != self.resultado_segun_criterio():
            raise DatosInvalidosError("El resultado no coincide con el criterio de aceptación del lote.")

        self.__estado = resultado


    def muestras_cerradas(self):
        return all(map(lambda muestra: True if muestra.getter_estado() in ("CONFORME", "NO_CONFORME") else False, self.__muestras))

    def tipos_defectos_dimensionales(self):
        tipos = set()
        for muestra in self.__muestras:
            inspeccion = muestra.getter_inspeccion()
            if inspeccion is not None and isinstance(inspeccion.getter_procedimiento(), ProcedimientoDimensional):
                tipos.update(map(lambda defecto: defecto.getter_tipo(), muestra.getter_defectos()))
        return tipos
    
    def restaurar_estado(self, estado):
        if estado not in ("PENDIENTE", "APROBADO", "RECHAZADO"):
            raise ValueError("Estado de lote inválido")
        self.__estado = estado


    def getter_estado(self):
        return self.__estado

    def getter_muestras(self):
        return self.__muestras.copy()

    def getter_id(self):
        return self.__ID
    def getter_cantidad_fabricada(self):
        return self.__cantidad_fabricada

