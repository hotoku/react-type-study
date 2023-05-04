import logging
import sys

import click

from . import db
from .server import app

LOGGER = logging.getLogger(__name__)


def setup_logging(debug: bool):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s",
        stream=sys.stderr
    )


@click.group
def main():
    setup_logging(True)
    db.clean()
    db.init()
    db.load()


@main.command
def start():
    app.run(debug=True, host="0.0.0.0", port=18889)


if __name__ == "__main__":
    main()
