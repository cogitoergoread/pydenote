"""Org-mode Journa converter"""

import argparse
import pathlib

from pydenote.attributes import Attributes
from pydenote.denote import DeNote
from pydenote.resources.__version__ import __version__ as __version__


class OrgJournal(DeNote):
    at: Attributes

    def process_infile(self) -> None:
        """Process Org journal file, line - by line"""
        for line in self.infile:
            if (line[:2] == "* ") or (line[:3] == "** ") or (line[:4] == "*** "):
                # Skip Heading 1..3
                # Do nothing
                pass
            elif line[:5] == "**** ":
                # Heading 4 starts a new day
                pass
            else:
                # Write the line to outfile
                print(line)

    def main(self) -> None:
        logstr = f"ojc (Org Journal Converter) version {__version__} starting..."
        print(logstr)
        parser = argparse.ArgumentParser(
            description="Convert Org-mode Journal file.",
            epilog="New Markdown files are placed to --journalhome or JOURNAL_HOME.",
        )
        parser.add_argument(
            "-i",
            "--infile",
            type=argparse.FileType("r", encoding="UTF-8"),
            required=True,
            help="Name of the Org Journal file",
        )
        parser.add_argument(
            "--journalhome", type=pathlib.Path, help="Folder of the journal files."
        )
        args = parser.parse_args()
        if not self.chk_dir(args.journalhome, "JOURNAL_HOME"):
            args.infile.close()
            exit(0)

        self.infile = args.infile
        self.process_infile()

        args.infile.close()


def main() -> None:
    oj = OrgJournal()
    oj.main()


if __name__ == "__main__":
    main()
