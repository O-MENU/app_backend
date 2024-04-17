from flask import Flask, request, jsonify
import json
import pandas as pd

app = Flask("MENU")

conn = """Conexão com MongoDB"""

#--------------------------- Root ----------------------------

#GET (/): Deve retornar "Hello, World!".
@app.route("/", methods=["GET"])
def hello_world():
    return "Hello, World!"
#-----------------------------------------------------------------