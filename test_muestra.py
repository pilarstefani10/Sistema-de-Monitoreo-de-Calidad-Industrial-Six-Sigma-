import pytest
from Muestra import Muestra
from Defecto import Defecto


def test_crear_muestra_correctamente():

    muestra = Muestra("M1", 10, "L1")

    assert muestra.ID == "M1"
    assert muestra.unidades_representadas == 10
    assert muestra.lote == "L1"
    assert muestra.estado == "PENDIENTE"
    assert muestra.defectos == []
    assert muestra.inspeccion is None


def test_muestra_con_unidades_invalidas():

    with pytest.raises(ValueError):
        Muestra("M1", 0, "L1")

    with pytest.raises(ValueError):
        Muestra("M2", -5, "L1")


def test_registrar_lista_de_defectos():

    muestra = Muestra("M1", 10, "L1")

    defecto1 = Defecto(
        "Desviacion dimensional",
        2,
        "La medida supera la tolerancia"
    )

    defecto2 = Defecto(
        "Anomalia visual",
        5,
        "Envase roto"
    )

    defectos = [defecto1, defecto2]

    muestra.registrar_defectos(defectos)

    assert len(muestra.defectos) == 2
    assert defecto1 in muestra.defectos
    assert defecto2 in muestra.defectos


def test_registrar_algo_que_no_sea_lista():

    muestra = Muestra("M1", 10, "L1")

    defecto = Defecto(
        "Anomalia visual",
        5,
        "Envase roto"
    )

    with pytest.raises(ValueError):
        muestra.registrar_defectos(defecto)

    assert muestra.defectos == []


def test_lista_con_elemento_que_no_es_defecto():

    muestra = Muestra("M1", 10, "L1")

    defecto = Defecto(
        "Anomalia visual",
        5,
        "Envase roto"
    )

    defectos = [
        defecto,
        "esto no es un defecto"
    ]

    with pytest.raises(ValueError):
        muestra.registrar_defectos(defectos)

    assert muestra.defectos == []


def test_no_agregar_defectos_a_muestra_cerrada():

    muestra = Muestra("M1", 10, "L1")

    muestra.estado = "CONFORME"

    defecto = Defecto(
        "Anomalia visual",
        5,
        "Envase roto"
    )

    with pytest.raises(ValueError):
        muestra.registrar_defectos([defecto])

    assert muestra.defectos == []