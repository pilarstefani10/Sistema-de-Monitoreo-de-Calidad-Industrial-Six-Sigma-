from unittest.mock import Mock
import pytest


def test_compara_tipos_comunes_y_exclusivos(administrador):
    administrador.empresa = Mock()

    lote1 = Mock()
    lote2 = Mock()

    lote1.tipos_defectos_dimensionales.return_value = {
        "Rayadura", "Golpe", "Mancha"
    }
    lote2.tipos_defectos_dimensionales.return_value = {
        "Golpe", "Oxido"
    }

    administrador.empresa.buscar_lote.side_effect = [lote1, lote2]

    comunes, solo1, solo2 = administrador.comparar_lotes("L1", "L2")

    assert comunes == {"Golpe"}
    assert solo1 == {"Rayadura", "Mancha"}
    assert solo2 == {"Oxido"}


def test_rechaza_mismo_lote(administrador):
    administrador.empresa = Mock()

    with pytest.raises(ValueError):
        administrador.comparar_lotes("L1", "L1")

    administrador.empresa.buscar_lote.assert_not_called()


def test_lotes_sin_defectos_comunes(administrador):
    administrador.empresa = Mock()

    lote1 = Mock()
    lote2 = Mock()

    lote1.tipos_defectos_dimensionales.return_value = {"Rayadura"}
    lote2.tipos_defectos_dimensionales.return_value = {"Golpe"}

    administrador.empresa.buscar_lote.side_effect = [lote1, lote2]

    comunes, solo1, solo2 = administrador.comparar_lotes("L1", "L2")

    assert comunes == set()
    assert solo1 == {"Rayadura"}
    assert solo2 == {"Golpe"}


def test_dos_lotes_vacios(administrador):
    administrador.empresa = Mock()

    lote1 = Mock()
    lote2 = Mock()

    lote1.tipos_defectos_dimensionales.return_value = set()
    lote2.tipos_defectos_dimensionales.return_value = set()

    administrador.empresa.buscar_lote.side_effect = [lote1, lote2]

    comunes, solo1, solo2 = administrador.comparar_lotes("L1", "L2")

    assert comunes == set()
    assert solo1 == set()
    assert solo2 == set()


def test_busca_los_dos_lotes(administrador):
    administrador.empresa = Mock()

    lote1 = Mock()
    lote2 = Mock()

    lote1.tipos_defectos_dimensionales.return_value = set()
    lote2.tipos_defectos_dimensionales.return_value = set()

    administrador.empresa.buscar_lote.side_effect = [lote1, lote2]

    administrador.comparar_lotes("L1", "L2")

    assert administrador.empresa.buscar_lote.call_count == 2
    administrador.empresa.buscar_lote.assert_any_call("L1")
    administrador.empresa.buscar_lote.assert_any_call("L2")


def test_consulta_cada_lote_una_vez(administrador):
    administrador.empresa = Mock()

    lote1 = Mock()
    lote2 = Mock()

    lote1.tipos_defectos_dimensionales.return_value = {"Rayadura"}
    lote2.tipos_defectos_dimensionales.return_value = {"Rayadura"}

    administrador.empresa.buscar_lote.side_effect = [lote1, lote2]

    administrador.comparar_lotes("L1", "L2")

    lote1.tipos_defectos_dimensionales.assert_called_once_with()
    lote2.tipos_defectos_dimensionales.assert_called_once_with()