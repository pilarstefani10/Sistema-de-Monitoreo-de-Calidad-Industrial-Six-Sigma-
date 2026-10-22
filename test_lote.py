import pytest
from unittest.mock import Mock


def test_tipos_dimensionales_sin_repetidos(lote):
    muestra = Mock()
    inspeccion = Mock()
    procedimiento = Mock()
    procedimiento.es_dimensional.return_value = True

    inspeccion.getter_procedimiento.return_value = procedimiento
    muestra.getter_inspeccion.return_value = inspeccion

    defecto1 = Mock()
    defecto1.getter_tipo.return_value = "Rayadura"

    defecto2 = Mock()
    defecto2.getter_tipo.return_value = "Desviacion"

    defecto3 = Mock()
    defecto3.getter_tipo.return_value = "Rayadura"

    muestra.getter_defectos.return_value = [defecto1, defecto2, defecto3]
    lote.getter_muestras = Mock(return_value=[muestra])

    assert lote.tipos_defectos_dimensionales() == {
        "Rayadura", "Desviacion"
    }


def test_lote_sin_muestras(lote):
    lote.getter_muestras = Mock(return_value=[])

    assert lote.tipos_defectos_dimensionales() == set()


def test_muestra_sin_inspeccion(lote):
    muestra = Mock()
    muestra.getter_inspeccion.return_value = None
    lote.getter_muestras = Mock(return_value=[muestra])

    assert lote.tipos_defectos_dimensionales() == set()


def test_procedimiento_no_dimensional(lote):
    muestra = Mock()
    inspeccion = Mock()
    procedimiento = Mock()
    procedimiento.es_dimensional.return_value = False

    inspeccion.getter_procedimiento.return_value = procedimiento
    muestra.getter_inspeccion.return_value = inspeccion
    lote.getter_muestras = Mock(return_value=[muestra])

    assert lote.tipos_defectos_dimensionales() == set()


def test_muestra_sin_defectos(lote):
    muestra = Mock()
    inspeccion = Mock()
    procedimiento = Mock()
    procedimiento.es_dimensional.return_value = True

    inspeccion.getter_procedimiento.return_value = procedimiento
    muestra.getter_inspeccion.return_value = inspeccion
    muestra.getter_defectos.return_value = []

    lote.getter_muestras = Mock(return_value=[muestra])

    assert lote.tipos_defectos_dimensionales() == set()