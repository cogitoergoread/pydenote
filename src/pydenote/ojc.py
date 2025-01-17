"""Org-mode Journa converter"""

import argparse
import pathlib

from pydenote.attributes import Attributes
from pydenote.resources.__version__ import __version__ as __version__


class OrgJournal:
    at: Attributes

    def ifile_check(self, filename: str) -> bool:
        """Check input org journal

        Args:
            filename (str): Name of the Org file, containing journal entries

        Returns:
            bool: File exists and valid
        """
        return True

    def main(self) -> None:
        logstr = f"ojc (Org Journal Converter) version {__version__} starting..."
        print(logstr)
        parser = argparse.ArgumentParser(
            description="Convert Org-mode Journal file.",
            epilog="New Markdown files are placed to --journalhome or JOURNAL_HOME.",
        )
        parser.add_argument("filename", help="Name of the Org Journal file")
        parser.add_argument(
            "--journalhome", type=pathlib.Path, help="Folder of the journal files."
        )
        args = parser.parse_args()
