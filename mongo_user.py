#create user
import pymongo
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
        'rest_preferidos':[],
        'comida_preferida':[],
        'amigos':[],	
        'localizacao':[], #{'data_hora': '', latitude': 0, 'longitude': 0}
        'rest_avaliados':[] #{'rest_id': 0, 'nota': 0}
      }
      db.counters.update_one({}, {'$inc':{'usuarios_id':1}})
      db.usuarios.insert_one(dic)
      return {'resp':{'message':'Usuario cadastrado com sucesso!', 'user': dic}, 'status_code': 201}
    return {'resp':'Erro: Usuario já existe!', 'status_code': 400}
  else:
    return {'resp':'Erro: Todos os campos são obrigatorios!', 'status_code': 400}

def rest_add(json):
  if campos_obrigatorios(json, ['nome', 'email', 'localizacao', 'cnpj', 'senha']):
    rest = db.usuarios.find_one({'cnpj' : json['cnpj']})
    if rest == None:
      dic = {
        '_id': 0,
        'nome': json['nome'],
        'email': json['email'],
        'localizacao': json['localizacao'], #endereço (rua, nº - bairro, cidade - sigla estado, cep)
        'cnpj': json['cnpj'], #se for microempreendimento aceitar cpf
        'senha': json['senha'],
        'nota': [],
        'categorias' : [],
        'cardapio' : '',
        'fotos' : [],
        'badges' : []
      }
      db.counters.update_one({}, {'$inc':{'restaurantes_id':1}})
      db.restaurantes.insert_one(dic)
      return {'resp':{'message':'Restaurante cadastrado com sucesso!', 'restaurante': dic}, 'status_code': 201}
    return {'resp':'Erro: Restaurante já existe!', 'status_code': 400}
  else:
    return {'resp':'Erro: Todos os campos são obrigatorios!', 'status_code': 400}
