from flask import Flask, request
import os
from mongo_user import *


app = Flask("MENU")

@app.route('/usuarios', methods=['POST'])
def cadastrar_usuario():
    nome = request.json.get('nome')
    email = request.json.get('email')
    data = request.json.get('data')
    senha = request.json.get('senha')
    #chamar funcao de validacao
    dic = user_add(nome, email, data, senha)
    return dic["resp"], dic["status_code"]

if __name__ == '__main__':
    app.run(debug=True)