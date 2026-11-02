from Lote import Lote
from unittest.mock import Mock


def test_lote_50_muestras_3_no_conformes_rechazado():

    # Creamos un lote de 50 unidades
    lote = Lote(50)

    # Creamos 50 muestras simuladas
    for i in range(50):

        muestra = Mock()

        # Cada muestra representa una unidad
        muestra.getter_unidadesrepresentadas.return_value = 1

        # La muestra pertenece al lote creado
        muestra.getter_lote.return_value = lote

        # Las primeras 3 muestras son NO_CONFORME
        if i < 3:
            muestra.getter_estado.return_value = "NO_CONFORME"
        else:
            muestra.getter_estado.return_value = "CONFORME"

        # Agregamos la muestra al lote
        lote.agregar_muestra(muestra)

    # Verificamos que el resultado sea RECHAZADO
    assert lote.resultado_segun_criterio() == "RECHAZADO"