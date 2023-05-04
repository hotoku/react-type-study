from __future__ import annotations
import logging
from .. import db
from . import app
import jsonschema as jss
from flask import jsonify, request
import json
from dataclasses import dataclass

LOGGER = logging.getLogger(__name__)


@app.get("/clients/<clid>")
def get(clid):
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


@dataclass(frozen=True)
class PostParam:
    name: str

    @staticmethod
    def create(payload: str) -> PostParam:
        schema = {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string"
                }
            },
            "required": [
                "name"
            ]
        }
        data = json.loads(payload)
        jss.validate(data, schema)
        return PostParam(
            data["name"]
        )


@app.post("/clients")
def post():
    payload = request.get_data().decode()
    try:
        param = PostParam.create(payload)
    except Exception as ex:
        return jsonify({
            "error": {
                "code": 400,
                "message": str(ex)
            }
        }), 400
    con = db.connection()
    try:
        # todo: 要サニタイズ
        sql = f"""
        insert into clients (
          name
        ) values (
          "{param.name}"
        )
"""
        LOGGER.debug("sql: %s", sql)
        db.execute(sql, con)
        sql2 = """
        select
          last_insert_rowid() as id
        from
          clients
"""
        df = db.query(sql2, con)
        con.commit()
        return jsonify({
            "success": {
                "code": 200,
                "message": f"successfully inserted id {df['id'].iloc[0]}"
            }
        }), 200
    except Exception as ex:
        con.rollback()
        return jsonify({
            "error": {
                "code": 500,
                "message": str(ex)
            }
        }), 500
