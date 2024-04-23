from flask import Flask, request
import os
from mongo_user import *
from mongo_rest import *

app = Flask("MENU")

#rotas usuarios
@app.route('/usuarios', methods=['POST'])
def cadastrar_usuario():
    json = request.json
    #chamar funcao de validacao
    dic = user_add(json)
    return dic["resp"], dic["status_code"]


@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    dic = user_find()
    return {'resp': dic["resp"], 'usuarios': dic['users']}, dic["status_code"]




#rotas restaurantes
@app.route('/restaurantes', methods=['POST'])
def cadastrar_restaurante():
    json = request.json
    #chamar funcao de validacao
    dic = rest_add(json)
    return dic["resp"], dic["status_code"]

@app.route('/restaurantes', methods=['GET'])
def listar_restaurantes():
    dic = rest_find()
    return {'resp': dic["resp"], 'restaurantes': dic['restaurantes']}, dic["status_code"]


if __name__ == '__main__':
    app.run(debug=True)