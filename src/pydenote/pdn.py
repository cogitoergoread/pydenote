"""Adding new Denote scheme note.
See original (Emacs lisp) docs at https://protesilaos.com/emacs/denote"""

import argparse
import os
import pathlib
import sys
from datetime import datetime

from pydenote.attributes import Attributes
from pydenote.denote import DeNote
from pydenote.resources.__version__ import __version__ as __version__


class NewNote(DeNote):
    at: Attributes

    def __init__(self) -> None:
        self.at = Attributes("", [], datetime.now(), "")

    def main(self) -> None:
        logstr = f"pdn (Python Denote new) version {__version__} starting..."
        print(logstr)
        parser = argparse.ArgumentParser(
            description="Create new denote file.",
            epilog="New Markdown file is placed to --denotehome or DENOTE_HOME.",
        )
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            "-j", "--journal", action="store_true", help="Create Journal entry"
        )
        group.add_argument("-t", "--title", type=str, help="Title of a note")

        parser.add_argument(
            "-k",
            "--keyword",
            type=str,
            help="keywords of a note, comma or whitespace separated string",
        )
        parser.add_argument(
            "-d",
            "--date",
            type=str,
            help="Date and time of a note, eg. 2024-12-31 23:59:59",
        )
        parser.add_argument(
            "--denotehome", type=pathlib.Path, help="Folder of the notes"
        )
        args = parser.parse_args()

        if args.date:
            if not self.at.set_date(args.date):
                print(f"Invalid date entered: {args.date}")
                exit(0)
        if args.keyword:
            self.at.set_keywords(args.keyword)
        if args.title:
            self.at.set_title(args.title)
        elif args.journal:
            self.at.set_journal()
        if not self.chk_dir(args.denotehome, "DENOTE_HOME"):
            exit(0)

        self.at.set_id()

        print("Type some text for your note. [Ctrl-D] to finish.")
        fname = os.path.join(self.path, self.at.get_filename())
        with open(fname, "w") as file:
            file.write(self.at.get_frontmatter())
            for line in sys.stdin:
                file.write(line)


def main() -> None:
    nn = NewNote()
    nn.main()


if __name__ == "__main__":
    main()
