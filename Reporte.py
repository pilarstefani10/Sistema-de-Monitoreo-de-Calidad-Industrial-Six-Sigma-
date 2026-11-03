
from Excepciones import TransicionInvalidaError
class Reporte:

    def __init__(self, ID, inspeccion):
        muestra = inspeccion.getter_muestra()

        if muestra.getter_estado() != "NO_CONFORME":
            raise TransicionInvalidaError("Solo se generan reportes para muestras No Conformes.")

        self.__ID = ID
        self.__inspeccion = inspeccion
        
        self.__defectos = tuple(map(
            lambda defecto: (
                defecto.getter_tipo(),
                defecto.getter_gravedad(),
                defecto.getter_descripcion()
            ),
            muestra.getter_defectos()
        ))



    def crear_resumen(self):
        muestra = self.__inspeccion.getter_muestra()

        resumen = "\nReporte: " + self.__ID + "\n"
        resumen += "Fecha: " + str(self.__inspeccion.getter_fecha()) + "\n"
        resumen += "Muestra: " + muestra.getter_id() + "\n"
        resumen += "Lote: " + muestra.getter_lote().getter_id() + "\n"
        resumen += "Responsable: " + self.__inspeccion.getter_profesional().getter_nombre() + "\n"
        resumen += "".join(map(lambda par: f"{par[0]}. Tipo: {par[1][0]} | Descripción: {par[1][2]} | Gravedad: {par[1][1]}\n", enumerate(self.__defectos, start=1)))

        return resumen

    def impacto_preliminar(self):
        lote = self.__inspeccion.getter_muestra().getter_lote()

        impacto = "\nImpacto preliminar en el lote " + lote.getter_id() + ":\n"
        impacto += f"  No conformes: {lote.porcentaje_preliminar():.1f}% de las muestras inspeccionadas (límite: 5%)\n"
        impacto += "  Si se evaluara hoy, el lote quedaría: " + lote.resultado_preliminar() + "\n"
        return impacto
    
    def getter_id(self):
        return self.__ID

    def getter_inspeccion(self):
        return self.__inspeccion

    def getter_defectos(self):
        return self.__defectos