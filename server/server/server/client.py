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
def get_client(clid):
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


@app.get("/clients")
def get_all_client():
    # todo: 要サニタイズ
    sql = f"""
select
    l.id as client_id,
    l.name as client_name,
    r.id as deal_id,
    r.name as deal_name
from
    clients l
      inner join
    deals r
      on l.id = r.client_id
"""
    ret = db.query(sql)

    clients = {}
    for r in range(len(ret)):
        cid = int(ret["client_id"].iloc[r])
        if cid not in clients:
            clients[cid] = {
                "id": cid,
                "name": ret["client_name"].iloc[r],
                "deals": []
            }
        cl = clients[cid]
        deal = {
            "id": int(ret["deal_id"].iloc[r]),
            "name": ret["deal_name"].iloc[r],
            "client_id": cid
        }
        cl["deals"].append(deal)

    return jsonify(list(clients.values()))


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
def post_client():
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


@dataclass(frozen=True)
class PutParam:
    id: int
    name: str

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
                }
            },
            "required": [
                "id",
                "name"
            ]
        }
        data = json.loads(payload)
        jss.validate(data, schema)
        return PutParam(
            data["id"],
            data["name"]
        )


@app.put("/clients")
def put_client():
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
        update clients
        set
          name="{param.name}"
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
