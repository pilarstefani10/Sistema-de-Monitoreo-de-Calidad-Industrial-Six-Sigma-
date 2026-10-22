
import pytest
from unittest.mock import Mock, patch, call

from Profesional import Profesional
from Inspeccion import Inspeccion
from Muestra import Muestra
from Procedimiento import Procedimiento
from Defecto import Defecto


# ==========================================
# FIXTURES
# ==========================================

@pytest.fixture
def profesional():
    return Profesional("Ana Perez")


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

    def _crear(profesional, unidades=3, resultados=None,
               estado_final="CONFORME"):

        if resultados is None:
            resultados = [None] * unidades

        muestra = Mock(spec=Muestra)
        muestra.getter_unidadesrepresentadas.return_value = unidades

        # Primera consulta: asignacion.
        # Segunda consulta: resultado posterior al cierre.
        muestra.getter_estado.side_effect = [
            "PENDIENTE", estado_final
        ]

        procedimiento = Mock(spec=Procedimiento)
        procedimiento.evaluar_unidad.side_effect = resultados

        inspeccion = Mock(spec=Inspeccion)
        inspeccion.getter_profesional.return_value = profesional
        inspeccion.getter_muestra.return_value = muestra
        inspeccion.getter_procedimiento.return_value = procedimiento
        inspeccion.getter_id.return_value = "I1"

        profesional.asignar_inspeccion(inspeccion)

        return inspeccion, muestra, procedimiento

    return _crear


# ==========================================
# EJECUCION DE UNIDADES
# ==========================================

def test_ejecutar_evalua_todas_las_unidades(
    profesional, crear_inspeccion
):
    inspeccion, muestra, procedimiento = crear_inspeccion(
        profesional, unidades=5
    )

    resultado = profesional.ejecutar_siguiente_inspeccion()

    assert procedimiento.evaluar_unidad.call_count == 5
    assert resultado is inspeccion


def test_ejecutar_una_sola_unidad(
    profesional, crear_inspeccion
):
    inspeccion, muestra, procedimiento = crear_inspeccion(
        profesional, unidades=1
    )

    profesional.ejecutar_siguiente_inspeccion()

    procedimiento.evaluar_unidad.assert_called_once_with()


def test_ejecutar_consulta_cantidad_unidades(
    profesional, crear_inspeccion
):
    inspeccion, muestra, procedimiento = crear_inspeccion(
        profesional
    )

    profesional.ejecutar_siguiente_inspeccion()

    muestra.getter_unidadesrepresentadas.assert_called_once()


# ==========================================
# REGISTRO DE DEFECTOS
# ==========================================

def test_ejecutar_filtra_los_none(
    profesional, crear_inspeccion, crear_defecto
):
    defecto1 = crear_defecto(2)
    defecto2 = crear_defecto(3)

    inspeccion, muestra, procedimiento = crear_inspeccion(
        profesional,
        unidades=5,
        resultados=[None, defecto1, None, defecto2, None]
    )

    profesional.ejecutar_siguiente_inspeccion()

    muestra.registrar_defectos.assert_called_once_with(
        [defecto1, defecto2]
    )


def test_ejecutar_sin_defectos(
    profesional, crear_inspeccion
):
    inspeccion, muestra, procedimiento = crear_inspeccion(
        profesional,
        resultados=[None, None, None]
    )

    profesional.ejecutar_siguiente_inspeccion()

    muestra.registrar_defectos.assert_called_once_with([])


def test_ejecutar_registra_todos_los_defectos(
    profesional, crear_inspeccion, crear_defecto
):
    defecto1 = crear_defecto(1)
    defecto2 = crear_defecto(3)
    defecto3 = crear_defecto(5)

    inspeccion, muestra, procedimiento = crear_inspeccion(
        profesional,
        resultados=[defecto1, defecto2, defecto3]
    )

    profesional.ejecutar_siguiente_inspeccion()

    muestra.registrar_defectos.assert_called_once_with(
        [defecto1, defecto2, defecto3]
    )


def test_ejecutar_registra_defectos_una_vez(
    profesional, crear_inspeccion
):
    inspeccion, muestra, procedimiento = crear_inspeccion(
        profesional
    )

    profesional.ejecutar_siguiente_inspeccion()

    muestra.registrar_defectos.assert_called_once()


# ==========================================
# INICIO Y CIERRE
# ==========================================

def test_ejecutar_inicia_inspeccion(
    profesional, crear_inspeccion
):
    inspeccion, muestra, procedimiento = crear_inspeccion(
        profesional
    )

    profesional.ejecutar_siguiente_inspeccion()

    muestra.iniciar_inspeccion.assert_called_once()


def test_ejecutar_cierra_muestra(
    profesional, crear_inspeccion
):
    inspeccion, muestra, procedimiento = crear_inspeccion(
        profesional
    )

    profesional.ejecutar_siguiente_inspeccion()

    muestra.cerrar.assert_called_once()


def test_ejecutar_respeta_orden_de_operaciones(
    profesional, crear_inspeccion
):
    inspeccion, muestra, procedimiento = crear_inspeccion(
        profesional
    )

    profesional.ejecutar_siguiente_inspeccion()

    operaciones = [
        llamada
        for llamada in muestra.method_calls
        if llamada[0] in (
            "iniciar_inspeccion",
            "registrar_defectos",
            "cerrar"
        )
    ]

    assert operaciones == [
        call.iniciar_inspeccion(),
        call.registrar_defectos([]),
        call.cerrar()
    ]


# ==========================================
# GENERACION DE REPORTES
# ==========================================

def test_ejecutar_conforme_no_genera_reporte(
    profesional, crear_inspeccion
):
    inspeccion, muestra, procedimiento = crear_inspeccion(
        profesional, estado_final="CONFORME"
    )

    with patch("Profesional.Reporte") as mock_reporte:
        profesional.ejecutar_siguiente_inspeccion()

    mock_reporte.assert_not_called()
    inspeccion.registrar_reporte.assert_not_called()


def test_ejecutar_no_conforme_genera_reporte(
    profesional, crear_inspeccion
):
    inspeccion, muestra, procedimiento = crear_inspeccion(
        profesional, estado_final="NO_CONFORME"
    )

    with patch("Profesional.Reporte") as mock_reporte:
        profesional.ejecutar_siguiente_inspeccion()

    mock_reporte.assert_called_once_with(
        "I1R", inspeccion
    )

    inspeccion.registrar_reporte.assert_called_once_with(
        mock_reporte.return_value
    )


def test_ejecutar_consulta_estado_final(
    profesional, crear_inspeccion
):
    inspeccion, muestra, procedimiento = crear_inspeccion(
        profesional
    )

    profesional.ejecutar_siguiente_inspeccion()

    assert muestra.getter_estado.call_count == 2


# ==========================================
# MANEJO DE ERRORES
# ==========================================

def test_ejecutar_error_al_iniciar(
    profesional, crear_inspeccion
):
    inspeccion, muestra, procedimiento = crear_inspeccion(
        profesional
    )

    muestra.iniciar_inspeccion.side_effect = ValueError(
        "Muestra ya inspeccionada"
    )

    with pytest.raises(ValueError, match="Muestra ya inspeccionada"):
        profesional.ejecutar_siguiente_inspeccion()

    muestra.registrar_defectos.assert_not_called()
    muestra.cerrar.assert_not_called()


def test_ejecutar_error_al_registrar(
    profesional, crear_inspeccion
):
    inspeccion, muestra, procedimiento = crear_inspeccion(
        profesional
    )

    muestra.registrar_defectos.side_effect = ValueError(
        "Error al registrar"
    )

    with pytest.raises(ValueError, match="Error al registrar"):
        profesional.ejecutar_siguiente_inspeccion()

    muestra.iniciar_inspeccion.assert_called_once()
    muestra.cerrar.assert_not_called()


def test_ejecutar_error_al_cerrar(
    profesional, crear_inspeccion
):
    inspeccion, muestra, procedimiento = crear_inspeccion(
        profesional
    )

    muestra.cerrar.side_effect = ValueError(
        "Error al cerrar"
    )

    with pytest.raises(ValueError, match="Error al cerrar"):
        profesional.ejecutar_siguiente_inspeccion()

    muestra.registrar_defectos.assert_called_once()
    inspeccion.registrar_reporte.assert_not_called()
