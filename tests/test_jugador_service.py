from app.services.jugador_service import normalize_pierna_habil


def test_normalize_pierna_habil_con_valores_largos():
    assert normalize_pierna_habil("Derecha") == "D"
    assert normalize_pierna_habil("Izquierda") == "I"
    assert normalize_pierna_habil("Ambas") == "A"
    assert normalize_pierna_habil("D") == "D"
    assert normalize_pierna_habil(None) is None
