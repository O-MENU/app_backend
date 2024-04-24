import pymongo
from utils import campos_obrigatorios

client = pymongo.MongoClient('mongodb+srv://henriquebrnetto02:2K4y7AIS4IOddUkC@menu.cyvtolc.mongodb.net/?retryWrites=true&w=majority&appName=MENU')

db = client['MENU']
counter = db.counters.find_one()
restaurante_id = counter['restaurantes_id']

def rest_add(json):
    if campos_obrigatorios(json, ['nome', 'email', 'localizacao', 'cnpj', 'senha']):
        rest = db.usuarios.find_one({'cnpj' : json['cnpj']})
        if rest == None:
            dic = {
            '_id': restaurante_id,
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
            return {'resp': 'Restaurante cadastrado com sucesso!', 'restaurante': dic, 'status_code': 201}
        return {'resp':'Erro: Restaurante já existe!', 'status_code': 400}
    else:
        return {'resp':'Erro: Todos os campos são obrigatorios!', 'status_code': 400}

def rest_find(id=None):
    if id == None:
        rests = db.restaurantes.find()
        return {'resp': 'Restaurantes encontrados com sucesso', 'restaurantes': list(rests), 'status_code': 200}
    else:
        rest = db.restaurantes.find_one({'_id': id})
        if rest == None:
            return {'resp': f'Erro: O restaurante <{id}> não existe', 'status_code': 404}
        else:
            return {'resp': f'Restaurante <{id}> encontrado com sucesso', 'restaurante': rest, 'status_code': 200}
