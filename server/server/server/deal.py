from flask import jsonify

from . import app
from .. import db


@app.get("/deals/<dlid>")
def deals(dlid):
    # todo: 要サニタイズ
    sql = f"""
select
    id,
    name,
    client_id
from
    deals
where
    id = {dlid}
"""
    ret = db.query(sql)
    return jsonify({
        "id": int(ret["id"].iloc[0]),
        "name": ret["name"].iloc[0],
        "client_id": int(ret["client_id"].iloc[0])
    })
