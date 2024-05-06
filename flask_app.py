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
    dic = user_add(json)
    # Inicializar objetos não inicializados no json passado ---> (rest_fav, seguidores, seguindo) <--- (localização já está sendo inicializada)
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

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def deleta_usuario(id):
    dic = user_delete(id)
    return dic['resp'], dic['status_code']

@app.route('/usuarios/<int:id1>/<int:id2>', methods=['PUT'])
def seguir_usuario(id1, id2):
    dic = user_seguir_add(id1, id2)
    return dic['resp'], dic['status_code']

@app.route('/usuarios/<int:id1>/<int:id2>', methods=['DELETE'])
def deixar_de_seguir(id1, id2):
    dic = user_seguir_delete(id1, id2)
    return dic['resp'], dic['status_code']

@app.route('/usuarios/<int:id>/comidas', methods=['PUT'])
def adicionar_comida_fav(id):
    comidas = request.list # LISTA !!!
    dic = user_comida_add(id, comidas)
    return dic['resp'], dic['status_code']

@app.route('/usuarios/<int:id>/comidas', methods=['DELETE'])
def deleta_comida_fav(id):
    comidas = request.list # LISTA !!!
    dic = user_comida_delete(id, comidas)
    return dic['resp'], dic['status_code']

@app.route('/usuarios/<int:id1>/restaurante/<int:id2>', methods=['PUT'])
def adiciona_rest_fav(id1, id2):
    dic = user_rest_add(id1, id2)
    return dic['resp'], dic['status_code']

@app.route('/usuarios/<int:id1>/restaurante/<int:id2>', methods=['DELETE'])
def deleta_rest_fav(id1, id2):
    dic = user_rest_delete(id1, id2)
    return dic['resp'], dic['status_code']

#                              V ---------  IMPORTANTE  ------------ V
#    -----> Fazer uma rota para atualizar (dar append) com  uma nova localização registrada do usuário <-------

#--------------------------------------------------------------------------------------------#
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

@app.route('/restaurantes/<int:id>/possiveis_clientes', methods=['GET'])
def listar_possiveis_clientes(id):
    dic = rest_possiveis_clientes(id)
    if dic["status_code"] == 200:
        return {'resp': dic["resp"], 'possiveis_clientes': dic['possiveis_clientes']}, dic["status_code"]
    return {'resp': dic["resp"]}, dic["status_code"]

@app.route('/restaurantes/<int:id>/adicionar_prato', methods=['PUT'])
def adiciona_prato(id):
    json = request.json
    dic = adicionar_prato(id, json)
    if dic["status_code"] == 201:
        return {'resp': dic["resp"], 'restaurante': dic['restaurante']}, dic["status_code"]
    return dic["resp"], dic["status_code"]

@app.route('/restaurantes/<int:id>/cardapio', methods=['GET'])
def find_cardapio(id):
    dic = get_cardapio(id)
    if dic["status_code"] == 200:
        return {'resp': dic["resp"], 'cardapio': dic['cardapio']}, dic["status_code"]
    return {'resp': dic["resp"]}, dic["status_code"]

@app.route('/restaurantes/<int:id>/prato/<int:id_prato>/adicionar_foto', methods=['PUT'])	
def add_foto(id, id_prato):
    json = request.json
    dic = adiciona_foto_prato(id, id_prato, json)
    if dic["status_code"] == 200:
        return {'resp': dic["resp"], 'restaurante': dic['restaurante']}, dic["status_code"]
    return dic["resp"], dic["status_code"]
  
#rotas restaurantes deletados
@app.route('/restaurantes_deletados', methods=['GET'])
def listar_restaurantes_deletados():
    dic = rest_deletado_find()
    return {'resp': dic["resp"], 'restaurantes_deletados': dic['restaurantes_deletados']}, dic["status_code"]


#--------------------------------------------------------------------------------------------#

# rotas avaliacoes

@app.route('/avaliacoes/usuarios/<int:id1>/restaurantes/<int:id2>')
def fazer_avaliacao_do_restaurante(id1, id2):
    json = request.json
    dic = user_avaliacao_add(id1, id2, json)
    return dic['resp'], dic['status_code']

@app.route('/avaliacoes', methods=['GET'])
def todas_as_avaliacoes():
    dic = avaliacao_find()
    return {'resp': dic['resp'], 'avaliacoes': dic['avaliacoes']}, dic['status_code']

@app.route('/avaliacoes/usuarios/<int:id>', methods=['GET'])
def avaliacoes_do_usuario(id):
    dic = avaliacao_find(id)
    if dic['status_code'] == 200:
        return {'resp': dic['resp'], 'avaliacoes': dic['avaliacoes']}, dic['status_code']
    else:
        return dic['resp'], dic['status_code']
    
@app.route('/avaliacoes/restaurantes/<int:id>',methods=['GET'])
def avaliacoes_do_restaurante(id):
    dic = avaliacao_find(None, id)
    if dic['status_code'] == 200:
        return {'resp': dic['resp'], 'avaliacoes': dic['avaliacoes']}, dic['status_code']
    else:
        return dic['resp'], dic['status_code']

@app.route('/avaliacoes/usuarios/<int:id1>/restaurantes/<int:id2>', methods=['GET'])
def avaliacao_usuario_restaurante(id1, id2):
    dic = avaliacao_find(id1, id2)
    if dic['status_code'] == 200:
        return {'resp': dic['resp'], 'avaliacao': dic['avaliacao']}, dic['status_code']
    else:
        return dic['resp'], dic['status_code']
      
      
#rota busca localizacao
@app.route('/get_loc/<string:end>', methods=['GET'])
def get_loc(end):
    loc = busca_loc(end)
    return {'resp': [loc['lat'], loc['lng']]}, 200

if __name__ == '__main__':
    app.run(debug=True)





