from pydenote.pdn import NewNote


def test_set_keywords() -> None:
    nn = NewNote()
    nn.set_keywords("Cica")
    assert nn.at.keywords == ["Cica"]
