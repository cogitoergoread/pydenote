"""Rename Denote files according to its frontmatter"""

import argparse
import os
import subprocess
import sys
from datetime import datetime

import frontmatter

from pydenote.attributes import Attributes
from pydenote.denote import DeNote
from pydenote.resources.__version__ import __version__ as __version__


class DenoteMove(DeNote):
    at: Attributes

    def process_infile(self) -> None:
        """Rename file based on frontmatter"""
        # Read toml frontmatter
        fm = frontmatter.load(self.infile)
        self.infile.close()

        # fm should have all keys
        if set(fm.keys()) != {"title", "date", "tags", "identifier"}:
            print(f"Frontmatter has not enough keys {fm.keys()}")
            exit(0)

        # Buld up attributes
        arr: list[str] = []
        arr = fm["tags"]  # type: ignore
        self.at = Attributes(
            str(fm["title"]),
            arr,
            datetime.strptime(str(fm["date"]), "%Y-%m-%dT%H:%M:%S"),
            "",
        )
        self.at.set_id()
        # Rename files based on mode
        if self.isosmv:
            # OS Rename
            source = os.path.join(self.filepath, self.filename)
            dest = os.path.join(self.filepath, self.at.get_filename())
            os.rename(source, dest)
            print(f"File {source} is os renamed to {dest}")
        else:
            # Git move
            cmd = f"git mv {self.filename} {self.at.get_filename()}"
            try:
                retcode = subprocess.call(cmd, shell=True, cwd=self.filepath)
                if retcode < 0:
                    print("Child was terminated by signal", -retcode, file=sys.stderr)
                else:
                    pass
            except OSError as e:
                print("Execution failed:", e, file=sys.stderr)
            print(f"File rename: {cmd}")

    def main(self) -> None:
        logstr = f"pmv ( PyDenote MoVe )  version {__version__} starting..."
        print(logstr)
        parser = argparse.ArgumentParser(
            description="Rename a Denote file according to its frontmatter",
            epilog="The file is renamed in place.",
        )
        parser.add_argument(
            "-i",
            "--infile",
            type=argparse.FileType("r", encoding="UTF-8"),
            required=True,
            help="Name of Denote file to be renamed.",
        )
        parser.add_argument(
            "-o",
            "--osmove",
            action="store_true",
            help="Use os 'mv' instead of default 'git mv'.",
        )
        args = parser.parse_args()
        print(f"OsMove:{args.osmove}")
        if args.osmove:
            self.isosmv = True
        else:
            self.isosmv = False
        self.infile = args.infile
        self.filename = os.path.basename(args.infile.name)
        self.filepath = os.path.dirname(args.infile.name)
        self.process_infile()


def main() -> None:
    pmv = DenoteMove()
    pmv.main()


if __name__ == "__main__":
    main()
