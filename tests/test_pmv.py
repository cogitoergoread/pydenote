import filecmp
import os
import pathlib
import shutil
import subprocess
import sys

import pytest

import pydenote
import pydenote.pmv


def test_main_nofile(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Emulating command line arguments, no file found"""
    myargs = ["--infile", "/ne.md"]
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
            pydenote.pmv.main()


def test_pmv_badfile(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Emulating command line arguments, no file found"""
    myargs = ["--infile", "tests/resources/sample_md_nokeysy.md"]
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
            pydenote.pmv.main()


def test_main_osrename(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Rename a file based on front matter"""
    infname = "sample_md_to_rename.md"
    oufname = (
        "20211027T054100--connections-of-notes_connection_note_ZettelkastenMethod.md"
    )
    inpath = os.path.join("tests/resources", infname)
    asspath = os.path.join("tests/resources", oufname)
    resultpath = os.path.join(tmp_path.__str__(), oufname)
    # Copy sample to tmp folder
    shutil.copy(inpath, tmp_path.__str__())

    myargs = ["--infile", os.path.join(tmp_path.__str__(), infname), "--osmove"]
    with monkeypatch.context() as m:
        m.setattr(
            sys,
            "argv",
            [
                "ojc",
            ]
            + myargs,
        )
        pydenote.pmv.main()

        assert filecmp.cmp(asspath, resultpath)


def test_main_gitrename(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Rename a file based on front matter via git mv"""
    infname = "sample_md_to_rename.md"
    oufname = (
        "20211027T054100--connections-of-notes_connection_note_ZettelkastenMethod.md"
    )
    inpath = os.path.join("tests/resources", infname)
    asspath = os.path.join("tests/resources", oufname)
    resultpath = os.path.join(tmp_path.__str__(), oufname)
    # Copy sample to tmp folder
    subprocess.call("git init .", shell=True, cwd=tmp_path.__str__())
    shutil.copy(inpath, tmp_path.__str__())
    subprocess.call(f"git add {infname}", shell=True, cwd=tmp_path.__str__())
    subprocess.call("git commit -m test -a", shell=True, cwd=tmp_path.__str__())

    myargs = ["--infile", os.path.join(tmp_path.__str__(), infname)]  # No "-o" arg!
    with monkeypatch.context() as m:
        m.setattr(
            sys,
            "argv",
            [
                "ojc",
            ]
            + myargs,
        )
        pydenote.pmv.main()

        assert filecmp.cmp(asspath, resultpath)
