from flask import Flask, request
import os
from mongo_user import *
from mongo_rest import *
from mongo_rest_deletados import *
app = Flask("MENU")

#rotas usuarios
@app.route('/usuarios', methods=['POST'])
def cadastrar_usuario():
    json = request.json
    #chamar funcao de validacao
    dic = user_add(json)
    return dic["resp"], dic["status_code"]


@app.route('/usuarios/<int:id>', methods=['GET'])
def listar_usuarios_por_id(id):
    dic = user_find(id)
    if dic["status_code"] == 200:
        return {'resp': dic["resp"], 'usuario': dic['user']}, dic["status_code"]
    return {'resp': dic["resp"]}, dic["status_code"]

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

@app.route('/restaurantes/<int:id>', methods=['GET'])
def listar_restaurante_por_id(id):
    dic = rest_find(id)
    if dic["status_code"] == 200:
        return {'resp': dic["resp"], 'restaurante': dic['restaurante']}, dic["status_code"]
    return {'resp': dic["resp"]}, dic["status_code"]

@app.route('/restaurantes/<int:id>', methods=['PUT'])
def editar_restaurante(id):
    json = request.json
    dic = rest_update(id, json)
    return dic["resp"], dic["status_code"]

@app.route('/restaurantes/<int:id>', methods=['DELETE', 'POST'])
def deletar_restaurante(id):
    dic = rest_delete(id)
    return dic["resp"], dic["status_code"]


#rotas restaurantes deletados
@app.route('/restaurantes_deletados', methods=['GET'])
def listar_restaurantes_deletados():
    dic = rest_deletado_find()
    return {'resp': dic["resp"], 'restaurantes_deletados': dic['restaurantes_deletados']}, dic["status_code"]

if __name__ == '__main__':
    app.run(debug=True)