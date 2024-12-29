from pydenote.pdn import NewNote


def test_set_title() -> None:
    nn = NewNote()
    nn.set_title("Cica")
    assert nn.at.title == "Cica"


def test_set_keywords() -> None:
    nn = NewNote()
    nn.set_keywords("Cica")
    assert nn.at.keywords == ["cica"]
    nn.set_keywords("Kapa?:,Vágás")
    assert nn.at.keywords == ["kapa", "vágás"]
    nn.set_keywords("$+!%÷Cica\n")
    assert nn.at.keywords == ["cica"]


def test_set_date() -> None:
    nn = NewNote()
    assert nn.set_date("2024.01.02")
    assert nn.at.date.__str__() == "2024-01-02"
    assert nn.set_date("2024.02.03 12.23:45")
    assert nn.at.date.__str__() == "2024-02-03 12:23:45"
    assert not nn.set_date("2024.02.03 12.23:75")
    assert not nn.set_date("2024.13.03 12.23:45")
    assert not nn.set_date("2024.02.30 12.23:45")
    assert not nn.set_date("2024.12.32 12.23:45")
    assert not nn.set_date("2024-13-12")
    assert not nn.set_date("Cica")
    assert not nn.set_date("2024.02+30 12.23:45")
    assert nn.set_date("20240304T235959")
    assert nn.at.date.__str__() == "2024-03-04 23:59:59"
