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
