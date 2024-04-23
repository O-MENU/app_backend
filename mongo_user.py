#create user
import pymongo
import pprint
from utils import campos_obrigatorios

client = pymongo.MongoClient('mongodb+srv://henriquebrnetto02:2K4y7AIS4IOddUkC@menu.cyvtolc.mongodb.net/?retryWrites=true&w=majority&appName=MENU')

db = client['MENU']
counter = db.counters.find_one()
usuario_id = counter['usuarios_id']

def user_add(json):
  if campos_obrigatorios(json, ['nome', 'email', 'data', 'senha']):
    user = db.usuarios.find_one({'email':json['email']})
    if user == None:
      dic = {
        '_id': usuario_id,
        'nome': json['nome'],
        'email': json['email'],
        'data': json['data'],
        'senha': json['senha'],
        'rest_fav': [],
        'comida_fav': [],
        'amigos': [],	
        'localizacao': [], #{'data_hora': '', latitude': 0, 'longitude': 0}
        'rest_avaliados':[] #{'rest_id': 0, 'nota': 0}
      }
      db.counters.update_one({}, {'$inc':{'usuarios_id':1}})
      db.usuarios.insert_one(dic)
      return {'resp':{'message':'Usuario cadastrado com sucesso!', 'user': dic}, 'status_code': 201}
    else:
      return {'resp':'Erro: Usuario já existe!', 'status_code': 400}
  else:
    return {'resp':'Erro: Todos os campos são obrigatorios!', 'status_code': 400}

def user_find(id=None):
  if id == None:
    users = db.usuarios.find()
    return {'resp': 'Usuarios encontrados com sucesso', 'users': list(users), 'status_code': 200}
  else:
    user = db.usuarios.find_one({'_id': id})
    if user == None:
      return {'resp': f'Erro: O usuario <{id}> não existe', 'status_code': 404}
    else:
      return {'resp': f'Usuario <{id}> encontrado com sucesso', 'user': user, 'status_code': 200}

def user_update(id, json):
  user = user_find(id)
  if user['status_code'] == 200:
    campos_possiveis = ['nome', 'email', 'data', 'senha']
    for key in json.keys():
      if key not in campos_possiveis:
        return {'resp': f'Erro: O campo <{key}> não é suportado', 'status_code': 404}
    for key in json.keys():
      db.usuarios.update_one({'_id': id}, {'$set': {key: json[key]}})
    return {'resp': f'Usuario <{id}> editado com sucesso', 'status_code': 200}
  else:
    return {'resp': f'Erro: O usuario <{id}> não existe', 'status_code': 404}

def user_delete(id):
  user = user_find(id)
  if user['status_code'] == 200:
    db.usuarios.delete_one({'_id': id})
    return {'resp': f'O usuario <{id}> foi deletado com sucesso', 'status_code': 200}
  else:
    return {'resp': f'Erro: O usuario <{id}> não existe', 'status_code': 404}

def user_amigo_add(usuario_id, amigo_id):
  user = user_find(usuario_id)
  amigo = user_find(amigo_id)
  if user['status_code'] == 200 and amigo['status_code'] == 200:
    user = user['user']
    amigo = amigo['user']
    for dic_amigo in user['amigos']:
      if amigo_id == dic_amigo['_id']:
        return {'resp': f'O usuario <{amigo_id}> (amigo) já esta na lista de amigos do usuario <{usuario_id}>', 'status_code': 400}

    db.usuarios.update_one({'_id': usuario_id}, {'$push': {'amigos': {'_id': amigo_id, 'nome': amigo['nome']}}})
    return {'resp': f'Usuario <{amigo_id}> (amigo) adicionado com sucesso ao usuario <{usuario_id}>', 'status_code': 200}
  else:
    return {'resp': f'Erro: Usuario <{usuario_id}> ou amigo <{amigo_id}> não existe', 'status_code': 404}

def user_comida_add(id, comida):
  user = user_find(id)
  if user['status_code'] == 200:
    user = user['user']
    db.usuarios.update_one({'_id': id}, {'$push': {'comida_fav': comida}})
    return {'resp': f'Comida <{comida}> adicionada ao usuario <{id}>', 'status_code': 200}
  else:
    return {'resp': f'Erro: O usuario <{id}> não existe', 'status_code': 404}
