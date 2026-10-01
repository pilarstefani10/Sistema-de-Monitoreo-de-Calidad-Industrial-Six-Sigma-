import pytest
from Muestra import Muestra
from Defecto import Defecto


def test_crear_muestra_correctamente():

    muestra = Muestra("M1", 10, "L1")

    assert muestra.getter_id() == "M1"
    assert muestra.getter_unidadesrepresentadas() == 10
    assert muestra.getter_lote() == "L1"
    assert muestra.getter_estado() == "PENDIENTE"
    assert muestra.getter_defectos() == []
    assert muestra.getter_inspeccion() is None


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

    assert len(muestra.getter_defectos()) == 2
    assert defecto1 in muestra.getter_defectos()
    assert defecto2 in muestra.getter_defectos()


def test_registrar_algo_que_no_sea_lista():

    muestra = Muestra("M1", 10, "L1")

    defecto = Defecto(
        "Anomalia visual",
        5,
        "Envase roto"
    )

    with pytest.raises(ValueError):
        muestra.registrar_defectos(defecto)

    assert muestra.getter_defectos() == []


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

    assert muestra.getter_defectos() == []

def test_registrar_lista_vacia():

    muestra = Muestra("M1", 10, "L1")

    muestra.registrar_defectos([])

    assert muestra.getter_defectos() == []

def test_lista_invalida_no_agrega_defectos_parcialmente():

    muestra = Muestra("M1", 10, "L1")

    defecto = Defecto(
        "Anomalia visual",
        3,
        "Envase rayado"
    )

    defectos = [
        defecto,
        "elemento invalido"
    ]

    with pytest.raises(ValueError):
        muestra.registrar_defectos(defectos)

    assert muestra.getter_defectos() == []

def test_getter_defectos_devuelve_copia():

    muestra = Muestra("M1", 10, "L1")

    defecto1 = Defecto(
        "Anomalia visual",
        2,
        "Envase rayado"
    )

    muestra.registrar_defectos([defecto1])

    lista_obtenida = muestra.getter_defectos()

    defecto2 = Defecto(
        "Anomalia visual",
        5,
        "Envase roto"
    )

    lista_obtenida.append(defecto2)

    assert len(lista_obtenida) == 2
    assert len(muestra.getter_defectos()) == 1
    assert defecto2 not in muestra.getter_defectos()

def test_no_cerrar_muestra_pendiente():

    muestra = Muestra("M1", 10, "L1")

    with pytest.raises(ValueError):
        muestra.cerrar()

    assert muestra.getter_estado() == "PENDIENTE"

def test_error_al_registrar_no_borra_defectos_anteriores():

    muestra = Muestra("M1", 10, "L1")

    defecto = Defecto(
        "Anomalia visual",
        2,
        "Envase rayado"
    )

    muestra.registrar_defectos([defecto])

    with pytest.raises(ValueError):
        muestra.registrar_defectos(["esto no es un defecto"])

    assert len(muestra.getter_defectos()) == 1
    assert defecto in muestra.getter_defectos()

def test_muestra_no_acepta_unidades_decimales():

    with pytest.raises(ValueError):
        Muestra("M1", 2.5, "L1")