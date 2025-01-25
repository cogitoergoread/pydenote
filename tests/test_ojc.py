import filecmp
import pathlib
import sys

import pytest

import pydenote.ojc


@pytest.mark.parametrize(
    "ps,rdt,rti",
    [
        (
            "**** [2020-07-09 Thu 05:59] Kedd - szerda, Éva el\n",
            "2020-07-09 05:59:00",
            "Kedd - szerda, Éva el",
        ),
        (
            "**** [2020-07-07 Tue 05:45]Vasárnap - hétfő\n",
            "2020-07-07 05:45:00",
            "Vasárnap - hétfő",
        ),
    ],
)
def test_parsehead(ps: str, rdt: str, rti: str) -> None:
    """Test Heading4 parser"""
    oj = pydenote.ojc.OrgJournal()
    retdt, retti = oj.parse_heading(ps)
    assert retdt.__str__() == rdt
    assert retti == rti


def test_main_nofile(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Emulating command line arguments, no file found"""
    myargs = ["--journalhome", tmp_path.__str__(), "--infile", "/ne.org"]
    with monkeypatch.context() as m:
        m.setattr(
            sys,
            "argv",
            [
                "ojc",
            ]
            + myargs,
        )
        with pytest.raises(SystemExit):
            pydenote.ojc.main()


def test_main_shortfile(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Emulating command line arguments, no file found"""
    myargs = [
        "--journalhome",
        tmp_path.__str__(),
        "--infile",
        "tests/resources/sample_short.org",
    ]
    with monkeypatch.context() as m:
        m.setattr(
            sys,
            "argv",
            [
                "ojc",
            ]
            + myargs,
        )
        pydenote.ojc.main()

        fname = "20200531T190600--2020-may_journal.md"
        assert filecmp.cmp(f"tests/resources/{fname}", f"{tmp_path.__str__()}/{fname}")
