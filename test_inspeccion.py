import pytest
from datetime import date

from Inspeccion import Inspeccion
from Muestra import Muestra
from Profesional import Profesional
from Certificacion import Certificacion
from Equipo import Equipo
from Procedimiento import Procedimiento
from Defecto import Defecto

# Procedimiento especial solamente para testing.
# Hereda de Procedimiento para que pase los isinstance del programa.
class ProcedimientoPrueba(Procedimiento):
#CAMBIAR POR MOCKS !!!!!!!!!!!!!!!!!

    def __init__(self, resultados, limite_gravedad=5):

        super().__init__(
            "Procedimiento de prueba",
            "volumen",
            "Control de leche",
            limite_gravedad
        )

        self.resultados = resultados
        self.indice = 0


    def evaluar_unidad(self):

        if self.indice < len(self.resultados):

            resultado = self.resultados[self.indice]

            self.indice += 1

            return resultado

        return None


# Esta función crea los objetos que necesitamos
# para hacer una inspección válida.
def crear_datos_base(resultados, limite_gravedad=5):

    fecha = date(2026, 9, 30)

    profesional = Profesional("Ana Perez")

    certificacion = Certificacion(
        "Control de leche",
        date(2026, 1, 1),
        date(2027, 1, 1)
    )

    profesional.agregar_certificacion(certificacion)

    equipo = Equipo(
        "volumen",
        date(2026, 8, 1)
    )

    procedimiento = ProcedimientoPrueba(
        resultados,
        limite_gravedad
    )

    muestra = Muestra(
        "M1",
        3,
        "L1"
    )

    return fecha, profesional, equipo, procedimiento, muestra


def test_crear_inspeccion_correctamente():

    fecha, profesional, equipo, procedimiento, muestra = crear_datos_base([])

    inspeccion = muestra.crear_inspeccion(
        fecha,
        profesional,
        equipo,
        procedimiento
    )

    assert isinstance(inspeccion, Inspeccion)

    assert inspeccion.getter_fecha() == fecha
    assert inspeccion.getter_profesional() is profesional
    assert inspeccion.getter_equipo() is equipo
    assert inspeccion.getter_procedimiento() is procedimiento
    assert inspeccion.getter_muestra() is muestra

    assert muestra.getter_estado() == "PENDIENTE"


def test_equipo_apto():

    fecha, profesional, equipo, procedimiento, muestra = crear_datos_base([])

    inspeccion = muestra.crear_inspeccion(
        fecha,
        profesional,
        equipo,
        procedimiento
    )

    assert inspeccion.equipo_apto() is True


def test_profesional_sin_certificacion():

    fecha = date(2026, 9, 30)

    profesional = Profesional("Ana Perez")

    equipo = Equipo(
        "volumen",
        date(2026, 8, 1)
    )

    procedimiento = ProcedimientoPrueba([])

    muestra = Muestra(
        "M1",
        3,
        "L1"
    )

    with pytest.raises(ValueError):

        muestra.crear_inspeccion(
            fecha,
            profesional,
            equipo,
            procedimiento
        )


def test_equipo_con_calibracion_vencida():

    fecha = date(2026, 9, 30)

    profesional = Profesional("Ana Perez")

    certificacion = Certificacion(
        "Control de leche",
        date(2026, 1, 1),
        date(2027, 1, 1)
    )

    profesional.agregar_certificacion(certificacion)

    equipo = Equipo(
        "volumen",
        date(2026, 1, 1)
    )

    procedimiento = ProcedimientoPrueba([])

    muestra = Muestra(
        "M1",
        3,
        "L1"
    )

    with pytest.raises(ValueError):

        muestra.crear_inspeccion(
            fecha,
            profesional,
            equipo,
            procedimiento
        )


def test_muestra_conforme():

    defecto = Defecto(
        "Defecto leve",
        1,
        "Defecto de gravedad baja"
    )

    resultados = [
        defecto,
        None,
        None
    ]

    fecha, profesional, equipo, procedimiento, muestra = crear_datos_base(
        resultados,
        limite_gravedad=3
    )

    inspeccion = muestra.crear_inspeccion(
        fecha,
        profesional,
        equipo,
        procedimiento
    )

    inspeccion.ejecutar()

    assert muestra.getter_estado() == "CONFORME"

    assert len(muestra.getter_defectos()) == 1


def test_muestra_no_conforme_por_defecto_critico():

    defecto_critico = Defecto(
        "Fisura",
        5,
        "Se encontró una fisura crítica"
    )

    resultados = [
        defecto_critico,
        None,
        None
    ]

    fecha, profesional, equipo, procedimiento, muestra = crear_datos_base(
        resultados,
        limite_gravedad=10
    )

    inspeccion = muestra.crear_inspeccion(
        fecha,
        profesional,
        equipo,
        procedimiento
    )

    inspeccion.ejecutar()

    assert muestra.getter_estado() == "NO_CONFORME"

    assert len(muestra.getter_defectos()) == 1


def test_muestra_no_conforme_por_suma_de_gravedades():

    defecto1 = Defecto(
        "Defecto A",
        2,
        "Primer defecto"
    )

    defecto2 = Defecto(
        "Defecto B",
        2,
        "Segundo defecto"
    )

    resultados = [
        defecto1,
        defecto2,
        None
    ]

    fecha, profesional, equipo, procedimiento, muestra = crear_datos_base(
        resultados,
        limite_gravedad=3
    )

    inspeccion = muestra.crear_inspeccion(
        fecha,
        profesional,
        equipo,
        procedimiento
    )

    inspeccion.ejecutar()

    # 2 + 2 = 4
    # 4 > límite 3
    assert muestra.getter_estado() == "NO_CONFORME"

    assert len(muestra.getter_defectos()) == 2


def test_suma_igual_al_limite_es_conforme():

    defecto1 = Defecto(
        "Defecto A",
        2,
        "Primer defecto"
    )

    defecto2 = Defecto(
        "Defecto B",
        1,
        "Segundo defecto"
    )

    resultados = [
        defecto1,
        defecto2,
        None
    ]

    fecha, profesional, equipo, procedimiento, muestra = crear_datos_base(
        resultados,
        limite_gravedad=3
    )

    inspeccion = muestra.crear_inspeccion(
        fecha,
        profesional,
        equipo,
        procedimiento
    )

    inspeccion.ejecutar()

    # 2 + 1 = 3
    # El código usa > y no >=
    assert muestra.getter_estado() == "CONFORME"