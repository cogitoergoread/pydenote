import pathlib
import sys

import pytest

import pydenote
import pydenote.zdc


def test_main_nofile(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Emulating command line arguments, no file found"""
    myargs = ["--denotehome", tmp_path.__str__(), "--infile", "/ne.md"]
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
            pydenote.zdc.main()


def test_main_samplefile(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Emulating command line arguments, given file"""
    myargs = [
        "--denotehome",
        tmp_path.__str__(),
        "--infile",
        "tests/resources/2021-10-27-0541 Connections of notes.md",
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
        pydenote.zdc.main()
        # fname = "20200531T190600--2020-may_journal.md"
        # assert filecmp.cmp(f"tests/resources/{fname}", f"{tmp_path.__str__()}/{fname}")
