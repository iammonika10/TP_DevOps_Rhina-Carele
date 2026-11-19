from pipeline.clean import convertir


def test_convertir_nombre():
    assert convertir("15.2") == 15.2
