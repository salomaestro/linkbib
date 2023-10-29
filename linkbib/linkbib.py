import argparse
import atexit
import logging
import logging.config
import logging.handlers
import sys
from pathlib import Path

from sqlitedict import SqliteDict


def parse_args():
    parser = argparse.ArgumentParser(description="docbib")
    subparsers = parser.add_subparsers(dest="command", help="link help")
    parser.add_argument("--debug", action="store_true", help="debug mode")

    link = subparsers.add_parser("link", help="link help")
    link.add_argument("doc", type=Path, help="doc file")
    link.add_argument("bib", type=argparse.FileType("r"), help="bib", default=sys.stdin)

    getbib = subparsers.add_parser("getbib", help="getbib help")
    getbib.add_argument("doc", type=Path, help="doc file", nargs="+")

    return parser.parse_args()


def init_loggers(log_to: Path):
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_formatter = logging.Formatter("%(levelname)s - %(message)s")

    file_handler = logging.handlers.RotatingFileHandler(
        log_to,
        maxBytes=1000000,
        backupCount=5,
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)

    root_logger = logging.getLogger(__file__)
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    return root_logger


class BibHandler:
    def __init__(self, bib_filebuf):
        self.bib_contents = self._read(bib_filebuf)

    @staticmethod
    def _read(open_file_buf):
        atexit.register(open_file_buf.close)
        with open_file_buf as f:
            return f.read()

    def shortname(self):
        return self.bib_contents.split("\n")[0].split("{")[1].split(",")[0]


class LinkBib:
    def __init__(self, database_path: Path, logger: logging.Logger):
        self.database_path = database_path
        self.logger = logger

    def link(self, doc: Path, bib: str):
        doc_name_key = doc.stem
        doc_entry = str(doc.absolute())
        bib_entry = BibHandler(bib)

        self.logger.debug(f"doc: {doc}")
        self.logger.debug(f"bib: {bib_entry.shortname()}")

        with SqliteDict(str(self.database_path), autocommit=True) as db:
            db[doc_name_key] = {"doc": doc_entry, "bib": bib_entry}

        self.logger.info(f"linked {doc} to {bib_entry.shortname()}")

    def getbib(self, docs: list[Path]):
        with SqliteDict(str(self.database_path), autocommit=True) as db:
            for doc in docs:
                self.logger.debug(f"doc: {doc}")

                doc_name_key = doc.stem
                doc_entry = db[doc_name_key]

                bib_entry = doc_entry["bib"]
                bib = bib_entry.bib_contents

                print(bib)


def main():
    # Setup
    root = Path().home() / ".linkbib"
    database_file = root / "linkbib.sqlite"
    log_file = root / "linkbib.log"

    root.mkdir(exist_ok=True)
    database_file.touch(exist_ok=True)
    log_file.touch(exist_ok=True)

    logger = init_loggers(log_file)

    app = LinkBib(database_file, logger)

    args = parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("debug mode")

    logger.debug(f"command: {args.command}")

    if args.command == "link":
        app.link(args.doc, args.bib)

    elif args.command == "getbib":
        app.getbib(args.doc)
