from __future__ import annotations
import logging
from .. import db
from . import app
import jsonschema as jss
from flask import jsonify, request
import json
from dataclasses import dataclass

LOGGER = logging.getLogger(__name__)


@app.get("/deals/<dlid>")
def get_deal(dlid):
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


@dataclass(frozen=True)
class PostParam:
    name: str
    client_id: int

    @staticmethod
    def create(payload: str) -> PostParam:
        schema = {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string"
                },
                "client_id": {
                    "type": "integer"
                }
            },
            "required": [
                "name",
                "client_id"
            ]
        }
        data = json.loads(payload)
        jss.validate(data, schema)
        return PostParam(
            data["name"],
            data["client_id"]
        )


@app.post("/deals")
def post_deal():
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
        insert into deals (
          name,
          client_id
        ) values (
          "{param.name}",
          {param.client_id}
        )
"""
        LOGGER.debug("sql: %s", sql)
        db.execute(sql, con)
        sql2 = """
        select
          last_insert_rowid() as id
        from
          deals
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


@dataclass(frozen=True)
class PutParam:
    id: int
    name: str
    client_id: int

    @staticmethod
    def create(payload: str) -> PutParam:
        schema = {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer"
                },
                "name": {
                    "type": "string"
                },
                "client_id": {
                    "type": "integer"
                }
            },
            "required": [
                "id",
                "name",
                "client_id"
            ]
        }
        data = json.loads(payload)
        jss.validate(data, schema)
        return PutParam(
            data["id"],
            data["name"],
            data["client_id"]
        )


@app.put("/deals")
def put_deal():
    payload = request.get_data().decode()
    try:
        param = PutParam.create(payload)
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
        update deals
        set
          name="{param.name}",
          client_id={param.client_id}
        where
          id={param.id}
"""
        LOGGER.debug("sql: %s", sql)
        db.execute(sql, con)
        con.commit()
        return jsonify({
            "success": {
                "code": 200,
                "message": f"successfully updated id {param.id}"
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
