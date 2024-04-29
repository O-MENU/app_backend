import pymongo
from utils import conn_mongo

client, db = conn_mongo()

def rest_deletado_find(id=None):
    if id == None:
        rests = db.restaurantes_deletados.find()
        return {'resp': 'Restaurantes deletados encontrados com sucesso', 'restaurantes_deletados': list(rests), 'status_code': 200}
    else:
        rest = db.restaurantes_deletados.find_one({'_id': id})
        if rest == None:
            return {'resp': f'Erro: O restaurante deletado <{id}> não existe', 'status_code': 404}
        else:
            return {'resp': f'Restaurante deletado <{id}> encontrado com sucesso', 'restaurante_deletado': rest, 'status_code': 200}
