import pytest

import pydenote.attributes


@pytest.mark.parametrize(
    "dstr",
    [
        "2024.02.03 12.23:75",
        "2024.13.03 12.23:45",
        "2024.02.30 12.23:45",
        "2024.12.32 12.23:45",
        "2024-13-12",
        "Cica",
        "2024.02+30 12.23:45",
    ],
)
def test_dc_sad(dstr: str) -> None:
    """Date checker sad path"""
    dc = pydenote.attributes.DateChecker(dstr)
    assert not dc.check_date()


@pytest.mark.parametrize(
    "dstr,res",
    [
        ("2024.01.02", "2024-01-02 00:00:00"),
        ("2024.02.03 12.23:45", "2024-02-03 12:23:45"),
        ("20240304T235959", "2024-03-04 23:59:59"),
    ],
)
def test_dc_happy(dstr: str, res: str) -> None:
    """Date checker happy path"""
    dc = pydenote.attributes.DateChecker(dstr)
    assert dc.check_date()
    assert dc.checked.__str__() == res
