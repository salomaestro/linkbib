# Linkbib

> Simple script for relating bibtex entry to document using sqlite

## Install

Installation is as simple as:

```sh
python3 -m pip install git@github.com:salomaestro/linkbib.git
```

This will add the command `linkbib` to your path.

## Example usage

### Linking a document to a bibtex entry

```sh
linkbib link path/to/document.pdf path/to/bibtex.bib
```

It is also possible to link a document to a text stream of bib contents:

```sh
cat my_bib.bib | linkbib link path/to/document -
```

### Viewing a bib entry

```sh
linkbib getbib path/to/document.pdf
```

However a full path is not neccesary, the database only uses the filename
without extension as the primary key in the database, hence,

```sh
linkbib getbib document
```

will also fetch the same entry.

### Database

The command stores entries in a sqlite3 database located in `~/.linkbib`. In
this directory there is also a log file.

## Future ideas/todo

1. Find a better way of linking multiple `.bib` files to multiple documents at
   the same time.
2. Research how to automagically update bibliography entries.
3. Possibly find a more intuitive key instead of using document name in database
   and for command, i.e. user specified or some other way.
