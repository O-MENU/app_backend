from flask import Flask, request
import os
from mongo_user import *


app = Flask("MENU")

@app.route('/usuarios', methods=['POST'])
def cadastrar_usuario():
    json = request.json
    #chamar funcao de validacao
    dic = user_add(json)
    return dic["resp"], dic["status_code"]

if __name__ == '__main__':
    app.run(debug=True)