import click

from . import db


@click.group
def main():
    db.clean()
    db.init()


@main.command
def start():
    db.load()


if __name__ == "__main__":
    main()
