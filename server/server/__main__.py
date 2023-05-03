import click

from . import db
from .server import app


@click.group
def main():
    db.clean()
    db.init()
    db.load()


@main.command
def start():
    app.run(debug=True, host="0.0.0.0", port=18888)


if __name__ == "__main__":
    main()
