import pytest
from Muestra import Muestra
from Defecto import Defecto
from Excepciones import DatosInvalidosError, TransicionInvalidaError

from unittest.mock import Mock
from Inspeccion import Inspeccion


@pytest.fixture
def muestra_en_inspeccion():

    muestra = Muestra("M1", 10, "L1")

    inspeccion = Mock(spec=Inspeccion)
    inspeccion.getter_muestra.return_value = muestra

    muestra.setter_inspeccion(inspeccion)
    muestra.iniciar_inspeccion()

    return muestra, inspeccion

def test_crear_muestra_correctamente():

    muestra = Muestra("M1", 10, "L1")

    assert muestra.getter_id() == "M1"
    assert muestra.getter_unidadesrepresentadas() == 10
    assert muestra.getter_lote() == "L1"
    assert muestra.getter_estado() == "PENDIENTE"
    assert muestra.getter_defectos() == []
    assert muestra.getter_inspeccion() is None


def test_muestra_con_unidades_invalidas():

    with pytest.raises(DatosInvalidosError):
        Muestra("M1", 0, "L1")

    with pytest.raises(DatosInvalidosError):
        Muestra("M2", -5, "L1")


def test_registrar_lista_de_defectos(muestra_en_inspeccion):

    muestra, inspeccion = muestra_en_inspeccion

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

    muestra.registrar_defectos(defectos, inspeccion)

    assert len(muestra.getter_defectos()) == 2
    assert defecto1 in muestra.getter_defectos()
    assert defecto2 in muestra.getter_defectos()


def test_registrar_algo_que_no_sea_lista(muestra_en_inspeccion):

    muestra, inspeccion = muestra_en_inspeccion

    defecto = Defecto(
        "Anomalia visual",
        5,
        "Envase roto"
    )

    with pytest.raises(DatosInvalidosError):
        muestra.registrar_defectos(defecto,inspeccion)

    assert muestra.getter_defectos() == []


def test_lista_con_elemento_que_no_es_defecto(muestra_en_inspeccion):

    muestra, inspeccion = muestra_en_inspeccion

    defecto = Defecto(
        "Anomalia visual",
        5,
        "Envase roto"
    )

    defectos = [
        defecto,
        "esto no es un defecto"
    ]

    with pytest.raises(DatosInvalidosError):
        muestra.registrar_defectos(defecto,inspeccion)

    assert muestra.getter_defectos() == []

def test_registrar_lista_vacia(muestra_en_inspeccion):

    muestra, inspeccion = muestra_en_inspeccion

    muestra.registrar_defectos([],inspeccion)

    assert muestra.getter_defectos() == []

def test_lista_invalida_no_agrega_defectos_parcialmente(muestra_en_inspeccion):

    muestra, inspeccion = muestra_en_inspeccion

    defecto = Defecto(
        "Anomalia visual",
        3,
        "Envase rayado"
    )

    defectos = [
        defecto,
        "elemento invalido"
    ]

    with pytest.raises(DatosInvalidosError):
        muestra.registrar_defectos(defecto,inspeccion)

    assert muestra.getter_defectos() == []

def test_getter_defectos_devuelve_copia(muestra_en_inspeccion):

    muestra, inspeccion = muestra_en_inspeccion

    defecto1 = Defecto(
        "Anomalia visual",
        2,
        "Envase rayado"
    )

    muestra.registrar_defectos([defecto1],inspeccion)

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

    with pytest.raises(TransicionInvalidaError):
        muestra.cerrar()

    assert muestra.getter_estado() == "PENDIENTE"

def test_error_al_registrar_no_borra_defectos_anteriores(muestra_en_inspeccion):

    muestra, inspeccion = muestra_en_inspeccion

    defecto = Defecto(
        "Anomalia visual",
        2,
        "Envase rayado"
    )

    muestra.registrar_defectos([defecto],inspeccion)

    with pytest.raises(DatosInvalidosError):
        muestra.registrar_defectos(["esto no es un defecto"],inspeccion)

    assert len(muestra.getter_defectos()) == 1
    assert defecto in muestra.getter_defectos()

def test_muestra_no_acepta_unidades_decimales():

    with pytest.raises(DatosInvalidosError):
        Muestra("M1", 2.5, "L1")

def test_no_registrar_defectos_en_muestra_pendiente():

    muestra = Muestra("M1", 10, "L1")

    inspeccion = Mock(spec=Inspeccion)
    inspeccion.getter_muestra.return_value = muestra

    muestra.setter_inspeccion(inspeccion)

    defecto = Defecto("Visual", 2, "Rayadura")

    with pytest.raises(TransicionInvalidaError):
        muestra.registrar_defectos([defecto], inspeccion)

    assert muestra.getter_defectos() == []

def test_no_registrar_defectos_de_otra_inspeccion(muestra_en_inspeccion):

    muestra, inspeccion = muestra_en_inspeccion

    otra_inspeccion = Mock(spec=Inspeccion)

    defecto = Defecto("Visual", 2, "Rayadura")

    with pytest.raises(TransicionInvalidaError):
        muestra.registrar_defectos(
            [defecto],
            otra_inspeccion
        )

    assert muestra.getter_defectos() == []