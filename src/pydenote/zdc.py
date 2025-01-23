"""ZettleDeft to Denote converter"""

import argparse
import os
import pathlib

from pydenote.attributes import Attributes, DateChecker
from pydenote.denote import DeNote
from pydenote.resources.__version__ import __version__ as __version__


class ZettleConv(DeNote):
    at: Attributes

    def process_infile(self) -> None:
        """Process ZettleDeft file, line - by line"""
        filename = os.path.basename(self.infile.name)
        split1 = filename.split(".")
        split2 = split1[0].split(" ")
        dtstr = "".join(split2[0].split("-")) + "00"
        title = " ".join(split2[1:])
        dc = DateChecker(dtstr)
        _ = dc.check_date()

        linenr = 0
        for line in self.infile:
            linenr += 1
            if linenr == 1:
                # First Line, Title, Skip
                pass
            elif linenr == 2:
                # Second line Optional keywords
                if line[0] == "#":
                    # Has real keywords
                    keywords = line[1:-1].split(" #")
                else:
                    keywords = []
                at = Attributes(title=title, date=dc.checked, keywords=keywords, id="")
                at.set_id()
                fname = os.path.join(self.path, at.get_filename())
                self.outfile = open(fname, "w")
                self.outfile.write(at.get_frontmatter())
                if line[0] != "#":
                    if self.outfile:
                        self.outfile.write(line)

            else:
                # Write the line to outfile
                if self.outfile:
                    self.outfile.write(line)

    def main(self) -> None:
        logstr = f"zdc (Zettle deft note converter) version {__version__} starting..."
        print(logstr)
        parser = argparse.ArgumentParser(
            description="Convert a ZettleDeft file to denote.",
            epilog="New Markdown file is placed to --denotehome or DENOTE_HOME.",
        )
        parser.add_argument(
            "-i",
            "--infile",
            type=argparse.FileType("r", encoding="UTF-8"),
            required=True,
            help="Name of ZettleDeft file",
        )
        parser.add_argument(
            "--denotehome", type=pathlib.Path, help="Folder of the notes"
        )
        args = parser.parse_args()

        if not self.chk_dir(args.denotehome, "DENOTE_HOME"):
            exit(0)

        self.infile = args.infile
        self.process_infile()

        args.infile.close()


def main() -> None:
    zc = ZettleConv()
    zc.main()


if __name__ == "__main__":
    main()
