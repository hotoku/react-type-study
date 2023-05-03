from flask import Flask, jsonify

from . import db

app = Flask(__name__)


@app.route("/hello")
def hello():
    return "hello\n"


@app.route("/clients/<clid>")
def clients(clid):
    # todo: 要サニタイズ
    sql = f"""
select
    id,
    name
from
    clients
where
    id = {clid}
"""
    ret = db.query(sql)
    return jsonify({
        "id": int(ret["id"].iloc[0]),
        "name": ret["name"].iloc[0]
    })
