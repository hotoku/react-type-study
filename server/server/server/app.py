from flask import Flask, jsonify

from .. import db

app = Flask(__name__)


@app.route("/hello")
def hello():
    return "hello\n"
