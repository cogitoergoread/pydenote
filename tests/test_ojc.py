import filecmp
import os
import pathlib
import sys
from collections.abc import Generator
from typing import Any
from unittest import mock

import pytest

from pydenote.ojc import main


@pytest.fixture
def mock_settings_env_vars() -> Generator[None, Any]:
    with mock.patch.dict(os.environ, {"JOURNAL_HOME": "/tmp"}):
        yield


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
            main()


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
        main()
        out, err = capsys.readouterr()

        print(out, err)
        fname = "20200531T190600--first-note_journal.md"
        assert filecmp.cmp(f"tests/resources/{fname}", f"{tmp_path.__str__()}/{fname}")
