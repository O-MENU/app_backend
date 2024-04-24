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
            'categorias' : [], #categoria perguntar marcelo
            'cardapio' : '', #fzr funcao para adicionar cardapio
            'fotos' : [], #fzr funcao para adicionar fotos
            'badges' : [] #perguntar pro biforus oq é
            }
            db.counters.update_one({}, {'$inc':{'restaurantes_id':1}})
            db.restaurantes.insert_one(dic)
            return {'resp':'Restaurante cadastrado com sucesso!', 'restaurante': dic, 'status_code': 201}
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

def rest_update(id, json):
    rest = rest_find(id)
    if rest['status_code'] == 200:
        campos_possiveis = ['nome', 'email', 'localizacao', 'cnpj', 'senha']
        for key in json.keys():
            if key not in campos_possiveis:
                return {'resp': f'Erro: O campo <{key}> não é suportado', 'status_code': 404}
        for key in json.keys():
            db.restaurantes.update_one({'_id': id}, {'$set': {key: json[key]}})
        return {'resp': f'Restaurante <{id}> editado com sucesso', 'status_code': 200}
    else:
        return {'resp': f'Erro: O restaurante <{id}> não existe', 'status_code': 404}
    
def rest_delete(id):
    rest = rest_find(id)
    if rest['status_code'] == 200:
        db.restaurantes_deletados.insert_one(rest['restaurante'])
        db.restaurantes.delete_one({'_id': id})
        return {'resp': f'Restaurante <{id}> deletado com sucesso', 'status_code': 200}
    else:
        return {'resp': f'Erro: O restaurante <{id}> não existe', 'status_code': 404}
