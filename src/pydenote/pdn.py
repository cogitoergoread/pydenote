"""Adding new Denote scheme note.
See original (Emacs lisp) docs at https://protesilaos.com/emacs/denote"""

import re
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=False)
class Attributes:
    title: str
    keywords: list[str]
    date: datetime
    id: str


class NewNote:
    at: Attributes

    def __init__(self) -> None:
        self.at = Attributes("", [], datetime.now(), "")

    def set_title(self, title: str) -> None:
        self.at.title = title

    def set_keywords(self, keywords: str) -> None:
        nkw = re.sub(r"\W+", " ", keywords).lower().strip()
        self.at.keywords = nkw.split(" ")

    def set_date(self, pdate: str) -> bool:
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
                self.at.date = datetime.strptime(dtstr, "%Y-%m-%d").date()
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
                self.at.date = datetime.strptime(dtstr, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return False
            return True

        return False
