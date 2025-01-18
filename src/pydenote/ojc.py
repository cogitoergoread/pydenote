"""Org-mode Journa converter"""

import argparse
import os
import pathlib
from datetime import datetime
from io import TextIOWrapper

from pydenote.attributes import Attributes, DateChecker
from pydenote.denote import DeNote
from pydenote.resources.__version__ import __version__ as __version__


class OrgJournal(DeNote):
    actdate: datetime
    outfile: TextIOWrapper | None

    def __init__(self) -> None:
        self.actdate = datetime.strptime("20010226110000", "%Y%m%d%H%M%S")
        self.outfile = None

    def parse_heading(self, headstr: str) -> tuple[datetime, str]:
        """Parse Org Heading 4 string to Title and date + time

        Args:
            headstr (str): Org capture, Heading 4, sample:
            "**** [2020-05-31 Sun 19:06] First note"

        Returns:
            tuple: ([Date], Title])
        """
        split1 = headstr[6:-1].split("]")
        split2 = split1[0].split(" ")
        dstr = f"{split2[0]} {split2[2]}:00"
        dc = DateChecker(dstr)
        _ = dc.check_date()
        return (dc.checked, split1[1].strip())

    def close(self) -> None:
        """Close outfile in case it is open."""
        if self.outfile:
            self.outfile.close()

    def chk_monthstart(self, ms: tuple[datetime, str]) -> None:
        """Checks the actual month and the new heading date. Start new file in case.

        Args:
            dt (datetime): Date from the heading
            title (str): Title
        """
        dt, title = ms
        if (dt.year == self.actdate.year) and (dt.month == self.actdate.month):
            # Same year and month as before
            pass
        else:
            self.close()
            self.actdate = dt
            # New file should be written
            at = Attributes(dt.strftime("%Y %B"), ["journal"], dt, "")
            at.set_id()
            print(f"Start new file, for month {dt.__str__()}.")
            fname = os.path.join(self.path, at.get_filename())
            self.outfile = open(fname, "w")
            self.outfile.write(at.get_frontmatter())
        if self.outfile:
            self.outfile.write(f"# {dt.__str__()} - {title}\n")

    def process_infile(self) -> None:
        """Process Org journal file, line - by line"""
        for line in self.infile:
            if (line[:2] == "* ") or (line[:3] == "** ") or (line[:4] == "*** "):
                # Skip Heading 1..3
                # Do nothing
                pass
            elif line[:5] == "**** ":
                # Heading 4 starts a new day
                self.chk_monthstart(self.parse_heading(line))
            else:
                # Write the line to outfile
                if self.outfile:
                    self.outfile.write(line)

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
