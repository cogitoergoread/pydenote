# pydenote
Utilities for Denote naming scheme notes.

## pdn

`pdn` is for creating a new note. Usage:

```text
usage: pdn [-h] [-j | -t TITLE] [-k KEYWORD] [-d DATE] [--denotehome DENOTEHOME]

Create new denote file.

options:
  -h, --help            show this help message and exit
  -j, --journal         Create Journal entry
  -t, --title TITLE     Title of a note
  -k, --keyword KEYWORD
                        keywords of a note, comma or whitespace separated string
  -d, --date DATE       Date and time of a note, eg. 2024-12-31 23:59:59
  --denotehome DENOTEHOME
                        Folder of the notes

New Markdown file is placed to --denotehome or DENOTE_HOME.
```
