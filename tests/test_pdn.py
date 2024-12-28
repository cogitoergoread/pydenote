from pydenote.pdn import NewNote


def test_set_keywords() -> None:
    nn = NewNote()
    nn.set_keywords("Cica")
    assert nn.at.keywords == ["cica"]
    nn.set_keywords("Kapa?:,Vágás")
    assert nn.at.keywords == ["kapa", "vágás"]
    nn.set_keywords("$+!%÷Cica\n")
    assert nn.at.keywords == ["cica"]
