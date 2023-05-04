import os
import pathlib as pl
import sqlite3
from typing import Any

import pandas as pd

_PATH = pl.Path(__file__).parent / "db.sqlite"


def clean():
    if os.path.exists(_PATH):
        os.remove(_PATH)


def init():
    con = sqlite3.connect(_PATH)
    con.executescript("""
create table clients (
    id integer primary key,
    name text not null
);
create table deals (
    id integer primary key,
    name text not null,
    client_id integer not null,
    is_finished boolean default false
);
""")


def load():
    clients = [("client-1",), ("client-2",), ("client-3",)]
    con = sqlite3.connect(_PATH)
    con.executemany("""
insert into clients (
    name
) values (
    ?
)
""", clients)

    def clients_gen():
        cur = 0
        while True:
            yield cur + 1
            cur += 1
            cur %= 3

    deals = [f"deal-{i}" for i in range(30)]
    con.executemany("""
insert into deals (
    name,
    client_id
) values (
    ?, ?
);
""", [(d, i) for d, i in zip(deals, clients_gen())])
    con.commit()


def query(sql: str, con=None) -> pd.DataFrame:
    if con is None:
        con = sqlite3.connect(_PATH)
    return pd.read_sql(sql, con)


def execute(sql: str, con=None):
    if con is None:
        con = sqlite3.connect(_PATH)
    con.execute(sql)


def connection() -> sqlite3.Connection:
    return sqlite3.connect(_PATH)
