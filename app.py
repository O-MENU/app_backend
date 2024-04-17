from flask import Flask, request, jsonify
import json
import pandas as pd
from utils import info_mongo

app = Flask("MENU")

info = info_mongo()
conn = """Conexão com MongoDB"""

#--------------------------- Root ----------------------------

#GET (/): Deve retornar "Hello, World!".
@app.route("/", methods=["GET"])
def hello_world():
    return "Hello, World!"
#-----------------------------------------------------------------