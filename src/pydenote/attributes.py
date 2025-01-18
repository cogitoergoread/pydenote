"""Adding new Denote scheme note.
See original (Emacs lisp) docs at https://protesilaos.com/emacs/denote"""

import re
from dataclasses import dataclass
from datetime import datetime

import toml
import yaml

from pydenote.resources.__version__ import __version__ as __version__


class DateChecker:
    indate: str
    checked: datetime

    def __init__(self, indate: str) -> None:
        self.indate = indate

    def check_date(self) -> bool:
        """Returns whether self.indate well formatted
            Sets self.checked with datetime value
            self.indate Good formatted date, eg 2024-12-24 23:59:59

        Returns:
            bool: Is pdate valid date
        """
        # Better (0[1-9]|1[0-2]) ([0-2][0-9]|3[01])
        fp_datum = re.compile(
            r"^(?P<year>\d{4})[\.\- ]?(?P<month>[01]\d)[\.\- ]?(?P<day>[0123]\d)$",
            re.UNICODE,
        )
        match = fp_datum.search(self.indate)
        if match is not None:
            # Short date found
            dtstr = f"{match.group('year')}-{match.group('month')}-{match.group('day')}"
            try:
                self.checked = datetime.strptime(dtstr, "%Y-%m-%d")
            except ValueError:
                return False
            return True
        # Date + Time
        fp_datum = re.compile(
            r"^(?P<year>\d{4})[\.\- ]?(?P<month>[01]\d)[\.\- ]?(?P<day>[0123]\d)[T ]?(?P<hour>\d{2})[\.\: ]?(?P<min>\d{2})[\.\: ]?(?P<sec>\d{2})$",
            re.UNICODE,
        )
        match = fp_datum.search(self.indate)

        if match is not None:
            # Date + Time found
            dtstr = f"{match.group('year')}-{match.group('month')}-{match.group('day')} {match.group('hour')}:{match.group('min')}:{match.group('sec')}"
            try:
                self.checked = datetime.strptime(dtstr, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return False
            return True

        return False


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
        dc = DateChecker(pdate)
        if dc.check_date():
            self.date = dc.checked
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
