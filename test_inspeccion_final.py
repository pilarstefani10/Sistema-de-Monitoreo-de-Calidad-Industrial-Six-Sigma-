
import pytest
from datetime import date
from unittest.mock import Mock, patch, call

from Inspeccion import Inspeccion
from Muestra import Muestra
from Profesional import Profesional
from Equipo import Equipo
from Procedimiento import Procedimiento
from Defecto import Defecto


@pytest.fixture
def crear_defecto():

    def _crear(gravedad):
        if type(gravedad) is not int or not 1 <= gravedad <= 5:
            raise ValueError("La gravedad debe estar entre 1 y 5")

        defecto = Mock(spec=Defecto)
        defecto.getter_gravedad.return_value = gravedad
        defecto.es_critico.return_value = gravedad == 5

        return defecto

    return _crear


@pytest.fixture
def crear_inspeccion():

    def _crear(unidades=3, limite=5, resultados=None):

        fecha = date(2026, 9, 30)

        profesional = Mock(spec=Profesional)
        profesional.certificaciones_faltantes.return_value = set()

        equipo = Mock(spec=Equipo)
        equipo.getter_ultima_calibracion.return_value = fecha
        equipo.getter_categoria.return_value = "dimensional"

        procedimiento = Mock(spec=Procedimiento)
        procedimiento.getter_certificaciones_requeridas.return_value = {"Metrologia"}        procedimiento.getter_categoria_equipo.return_value = "dimensional"
        procedimiento.getter_limitegravedad.return_value = limite

        if resultados is None:
            resultados = [None] * unidades

        procedimiento.evaluar_unidad.side_effect = resultados

        muestra = Mock(spec=Muestra)
        muestra.getter_unidadesrepresentadas.return_value = unidades
        muestra.getter_defectos.return_value = []
        muestra.getter_estado.return_value = "CONFORME"

        inspeccion = Inspeccion(
            "I1", fecha, profesional, equipo,
            procedimiento, muestra
        )

        return inspeccion, muestra, procedimiento

    return _crear



# ==========================================
# TESTS DE CONFORMIDAD
# ==========================================

def test_conformidad_sin_defectos(crear_inspeccion):
    inspeccion, muestra, procedimiento = crear_inspeccion()

    muestra.getter_defectos.return_value = []

    assert inspeccion.conformidad() is True


def test_conformidad_suma_menor_al_limite(
    crear_inspeccion, crear_defecto
):
    inspeccion, muestra, procedimiento = crear_inspeccion(limite=5)

    defecto1 = crear_defecto(1)
    defecto2 = crear_defecto(2)

    muestra.getter_defectos.return_value = [defecto1, defecto2]

    assert inspeccion.conformidad() is True


def test_conformidad_suma_igual_al_limite(
    crear_inspeccion, crear_defecto
):
    inspeccion, muestra, procedimiento = crear_inspeccion(limite=5)

    defecto1 = crear_defecto(2)
    defecto2 = crear_defecto(3)

    muestra.getter_defectos.return_value = [defecto1, defecto2]

    assert inspeccion.conformidad() is True


def test_conformidad_suma_mayor_al_limite(
    crear_inspeccion, crear_defecto
):
    inspeccion, muestra, procedimiento = crear_inspeccion(limite=5)

    defecto1 = crear_defecto(2)
    defecto2 = crear_defecto(4)

    muestra.getter_defectos.return_value = [defecto1, defecto2]

    assert inspeccion.conformidad() is False


def test_conformidad_defecto_critico(
    crear_inspeccion, crear_defecto
):
    inspeccion, muestra, procedimiento = crear_inspeccion(limite=10)

    defecto = crear_defecto(5)

    muestra.getter_defectos.return_value = [defecto]

    assert inspeccion.conformidad() is False


def test_conformidad_critico_con_suma_igual_al_limite(
    crear_inspeccion, crear_defecto
):
    inspeccion, muestra, procedimiento = crear_inspeccion(limite=5)

    defecto = crear_defecto(5)

    muestra.getter_defectos.return_value = [defecto]

    assert inspeccion.conformidad() is False


def test_conformidad_consulta_gravedad_de_todos_los_defectos(
    crear_inspeccion, crear_defecto
):
    inspeccion, muestra, procedimiento = crear_inspeccion()

    defecto1 = crear_defecto(1)
    defecto2 = crear_defecto(2)
    defecto3 = crear_defecto(3)

    muestra.getter_defectos.return_value = [
        defecto1, defecto2, defecto3
    ]

    inspeccion.conformidad()

    defecto1.getter_gravedad.assert_called_once()
    defecto2.getter_gravedad.assert_called_once()
    defecto3.getter_gravedad.assert_called_once()


def test_conformidad_consulta_si_hay_defectos_criticos(
    crear_inspeccion, crear_defecto
):
    inspeccion, muestra, procedimiento = crear_inspeccion()

    defecto1 = crear_defecto(2)
    defecto2 = crear_defecto(5)

    muestra.getter_defectos.return_value = [defecto1, defecto2]

    assert inspeccion.conformidad() is False

    defecto1.es_critico.assert_called_once()
    defecto2.es_critico.assert_called_once()


def test_conformidad_consulta_limite_del_procedimiento(
    crear_inspeccion, crear_defecto
):
    inspeccion, muestra, procedimiento = crear_inspeccion(limite=5)

    muestra.getter_defectos.return_value = [
        crear_defecto(2),
        crear_defecto(4)
    ]

    inspeccion.conformidad()

    procedimiento.getter_limitegravedad.assert_called_once()


def test_conformidad_no_modifica_muestra(
    crear_inspeccion, crear_defecto
):
    inspeccion, muestra, procedimiento = crear_inspeccion()

    muestra.getter_defectos.return_value = [
        crear_defecto(2)
    ]

    inspeccion.conformidad()

    muestra.registrar_defectos.assert_not_called()
    muestra.iniciar_inspeccion.assert_not_called()
    muestra.cerrar.assert_not_called()