"""Adding new Denote scheme note.
See original (Emacs lisp) docs at https://protesilaos.com/emacs/denote"""

import argparse
import os
import pathlib
import re
import sys
from dataclasses import dataclass
from datetime import datetime

import toml
import yaml

from pydenote.resources.__version__ import __version__ as __version__


@dataclass(frozen=False)
class Attributes:
    title: str
    keywords: list[str]
    date: datetime
    id: str

    def set_title(self, title: str) -> None:
        """Set title attribute and clean the whitespace characters

        Args:
            title (str): Title string
        """
        self.title = re.sub(r"\W+", " ", title).strip()

    def set_keywords(self, keywords: str) -> None:
        """Sets Keyword attribut and clean from whitespaces

        Args:
            keywords (str): _description_
        """
        nkw = re.sub(r"\W+", " ", keywords).lower().strip()
        self.keywords = nkw.split(" ")

    def set_date(self, pdate: str) -> bool:
        """Checks the 'date' parameter

        Args:
            pdate (str): Good formatted date, eg 2024-12-24 23:59:59

        Returns:
            bool: Is pdate valid date
        """
        # Better (0[1-9]|1[0-2]) ([0-2][0-9]|3[01])
        fp_datum = re.compile(
            r"^(?P<year>\d{4})[\.\- ]?(?P<month>[01]\d)[\.\- ]?(?P<day>[0123]\d)$",
            re.UNICODE,
        )
        match = fp_datum.search(pdate)
        if match is not None:
            # Short date found
            dtstr = f"{match.group('year')}-{match.group('month')}-{match.group('day')}"
            try:
                self.date = datetime.strptime(dtstr, "%Y-%m-%d")
            except ValueError:
                return False
            return True
        # Date + Time
        fp_datum = re.compile(
            r"^(?P<year>\d{4})[\.\- ]?(?P<month>[01]\d)[\.\- ]?(?P<day>[0123]\d)[T ]?(?P<hour>\d{2})[\.\: ]?(?P<min>\d{2})[\.\: ]?(?P<sec>\d{2})$",
            re.UNICODE,
        )
        match = fp_datum.search(pdate)

        if match is not None:
            # Date + Time found
            dtstr = f"{match.group('year')}-{match.group('month')}-{match.group('day')} {match.group('hour')}:{match.group('min')}:{match.group('sec')}"
            try:
                self.date = datetime.strptime(dtstr, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return False
            return True

        return False

    def set_id(self) -> None:
        """ID is a formatted datetime"""
        self.id = self.date.strftime("%Y%m%dT%H%M%S")

    def set_journal(self) -> None:
        """Journal entries have special title and keyword"""
        self.keywords.append("journal")
        if len(self.title) == 0:
            self.set_title(self.date.strftime("%A %d %B %Y"))

    def get_frontmatter(self, istoml: bool = True) -> str:
        """Create either TOML or YAML formatted front matter

        Args:
            istoml (bool, optional): Toml (True)/ YAML (False). Defaults to True.

        Returns:
            str: Pretty formatted frontmatter
        """
        oudi = {
            "title": self.title,
            "date": self.date.strftime("%Y-%m-%dT%H:%M:%S"),
            "tags": self.keywords,
            "identifier": self.id,
        }
        if istoml:
            rets = f"+++\n{toml.dumps(oudi)}+++\n"
        else:
            rets = f"---\n{yaml.dump(oudi)}---\n"
        return rets

    def get_filename(self) -> str:
        """Create a filename from the attributes
        example: 20220610T062201--define-type__denote_emacs_package.md

        Returns:
            str: Denote filename
        """
        stit = re.sub(r"\W+", "-", self.title).lower().strip()
        skey = "_".join(self.keywords)
        return f"{self.id}--{stit}_{skey}.md"


class NewNote:
    at: Attributes

    def __init__(self) -> None:
        self.at = Attributes("", [], datetime.now(), "")

    def chk_dir(self, dir: str) -> bool:
        home_dir = dir if dir else os.environ.get("DENOTE_HOME", ".")
        if not os.path.exists(home_dir) or not os.access(home_dir, os.W_OK):
            print(f"Folder {home_dir} is not ready for writing files.")
            return False
        self.path = home_dir
        return True

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
        parser.add_argument("--denotehome", type=pathlib.Path)
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
        if not self.chk_dir(args.denotehome):
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
