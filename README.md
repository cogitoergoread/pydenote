# pydenote
Utilities for Denote naming scheme notes.

See the original Emacs related manual, written by Protesilaos Stavrou: <https://protesilaos.com/emacs/denote>

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

## ojc

Org-mode journal converter. Usage:

```text
usage: ojc [-h] -i INFILE [--journalhome JOURNALHOME]

Convert Org-mode Journal file.

options:
  -h, --help            show this help message and exit
  -i, --infile INFILE   Name of the Org Journal file
  --journalhome JOURNALHOME
                        Folder of the journal files.

New Markdown files are placed to --journalhome or JOURNAL_HOME.
```

## zdc

Zettedeft ote conversion to Denote.

```text
zdc -h
zdc (Zettle deft note converter) version 1.0.1.dev2 starting...
usage: zdc [-h] -i INFILE [--denotehome DENOTEHOME]

Convert a ZettleDeft file to denote.

options:
  -h, --help            show this help message and exit
  -i, --infile INFILE   Name of ZettleDeft file
  --denotehome DENOTEHOME
                        Folder of the notes

New Markdown file is placed to --denotehome or DENOTE_HOME.
```
