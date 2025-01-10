"""Python Denote New command tests"""

import io
import os
from collections.abc import Generator
from pathlib import Path
import pathlib
import sys
from typing import Any
from unittest import mock

import pytest

from pydenote.pdn import NewNote, main


@pytest.fixture
def mock_settings_env_vars() -> Generator[None, Any]:
    with mock.patch.dict(os.environ, {"DENOTE_HOME": "/tmp"}):
        yield


def test_set_title() -> None:
    nn = NewNote()
    nn.at.set_title("Cica")
    assert nn.at.title == "Cica"
    nn.at.set_title("$+!%÷Cica\n")
    assert nn.at.title == "Cica"


def test_set_keywords() -> None:
    nn = NewNote()
    nn.at.set_keywords("Cica")
    assert nn.at.keywords == ["cica"]
    nn.at.set_keywords("Kapa?:,Vágás")
    assert nn.at.keywords == ["kapa", "vágás"]
    nn.at.set_keywords("$+!%÷Cica\n")
    assert nn.at.keywords == ["cica"]


def test_set_date() -> None:
    nn = NewNote()
    assert nn.at.set_date("2024.01.02")
    assert nn.at.date.__str__() == "2024-01-02 00:00:00"
    assert nn.at.set_date("2024.02.03 12.23:45")
    assert nn.at.date.__str__() == "2024-02-03 12:23:45"
    assert not nn.at.set_date("2024.02.03 12.23:75")
    assert not nn.at.set_date("2024.13.03 12.23:45")
    assert not nn.at.set_date("2024.02.30 12.23:45")
    assert not nn.at.set_date("2024.12.32 12.23:45")
    assert not nn.at.set_date("2024-13-12")
    assert not nn.at.set_date("Cica")
    assert not nn.at.set_date("2024.02+30 12.23:45")
    assert nn.at.set_date("20240304T235959")
    assert nn.at.date.__str__() == "2024-03-04 23:59:59"


def test_set_id() -> None:
    nn = NewNote()
    assert nn.at.set_date("2024.02.03 12.23:45")
    assert nn.at.date.__str__() == "2024-02-03 12:23:45"
    nn.at.set_id()
    assert nn.at.id == "20240203T122345"


@pytest.fixture
def journal() -> NewNote:
    nn = NewNote()
    assert nn.at.set_date("2024.02.03 12.23:45")
    nn.at.set_journal()
    nn.at.set_id()
    return nn


@pytest.mark.parametrize(
    "ismd,res",
    [
        (
            True,
            """+++
title = "Saturday 03 February 2024"
date = "2024-02-03T12:23:45"
tags = [ "journal",]
identifier = "20240203T122345"
+++
""",
        ),
        (
            False,
            """---
date: '2024-02-03T12:23:45'
identifier: 20240203T122345
tags:
- journal
title: Saturday 03 February 2024
---
""",
        ),
    ],
)
def test_get_frontmatter(ismd: bool, res: str, journal: NewNote) -> None:
    ret = journal.at.get_frontmatter(ismd)
    assert ret == res


def test_get_filename(journal: NewNote) -> None:
    fname = "20240203T122345--saturday-03-february-2024_journal.md"
    assert journal.at.get_filename() == fname


def test_chk_dir_param() -> None:
    nn = NewNote()
    assert nn.chk_dir("/tmp")
    assert not nn.chk_dir("/bin")


def test_chk_dir_envir(mock_settings_env_vars: Generator[None, Any]) -> None:
    nn = NewNote()
    assert nn.chk_dir("")

def test_main(monkeypatch:pytest.MonkeyPatch,tmp_path:pathlib.Path) -> None:
    """Mintha parancssorból hívtuk volna
    """
    myargs=[ "--denotehome", tmp_path.__str__(), "-t", "titlesample", "-k", "keysample", "-d", "20241231T235959"]
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['pdn', ]+ myargs)
        m.setattr('sys.stdin', io.StringIO('Cica'))

        main()

    note="""+++
title = "titlesample"
date = "2024-12-31T23:59:59"
tags = [ "keysample",]
identifier = "20241231T235959"
+++
Cica"""
    p = tmp_path / "20241231T235959--titlesample_keysample.md"
    assert p.read_text(encoding="utf-8") == note
