import pymongo
from utils import campos_obrigatorios, conn_mongo, busca_loc

client, db = conn_mongo()

counter = db.counters.find_one()
restaurante_id = counter['restaurantes_id']
prato_id = counter['pratos_id']

def rest_add(json):
    if campos_obrigatorios(json, ['nome', 'email', 'localizacao', 'cnpj', 'senha', 'categorias']):
        rest = db.restaurantes.find_one({'cnpj' : json['cnpj']})
        if rest == None:
            dic = {
            '_id': restaurante_id,
            'nome': json['nome'],
            'email': json['email'],
            'localizacao': {'endereco' : json['localizacao'], 'geoloc' : busca_loc(json['localizacao'])}, #endereço (rua, nº - bairro, cidade - sigla estado, cep)
            'cnpj': json['cnpj'], #se for microempreendimento aceitar cpf
            'senha': json['senha'],
            'categorias': json['categorias'], #categoria perguntar marcelo
            'nota': [],
            'cardapio' : [], #fzr funcao para adicionar cardapio formato [{"nome_prato":nome, "preco":preco, "descricao":descricao, "fotos":[]}...]
            'fotos' : [], #fzr funcao para adicionar fotos
            'badges' : [], #perguntar pro biforus oq é
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
            if key == 'localizacao':
                db.restaurantes.update_one({'_id': id}, {'$set': {key: {'endereco' : json[key], 'geoloc' : busca_loc(json[key])}}})
            else:
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

def adicionar_prato(id, json):
    rest = rest_find(id)
    if rest['status_code'] == 200:
        for prato in rest['restaurante']['cardapio']:
            if prato['nome_prato'] == json['nome_prato']:
                return {'resp': f'Erro: O prato <{json["nome_prato"]}> já existe', 'status_code': 400}
        if campos_obrigatorios(json, ['nome_prato', 'preco', 'descricao']):
            dic = {
                '_id': prato_id,
                'nome_prato': json['nome_prato'],
                'preco': json['preco'],
                'descricao': json['descricao'],
                'foto_prato': []
            }
            db.counters.update_one({}, {'$inc': {'pratos_id': 1}})
            db.restaurantes.update_one({'_id': id}, {'$push': {'cardapio': dic}})
            return {'resp': f'Prato adicionado ao restaurante <{id}> com sucesso', 'status_code': 201, 'restaurante': rest['restaurante']}
        else:
            return {'resp': f'Erro: Todos os campos são obrigatorios!', 'status_code': 400}
    else:
        return {'resp': f'Erro: O restaurante <{id}> não existe', 'status_code': 404}

def deleta_prato(rest_id, id_prato):
    rest = rest_find(rest_id)
    if rest['status_code'] == 200:
        for prato in rest['restaurante']['cardapio']:
            if id_prato == prato['_id']:
                db.restaurantes.update_one({'_id': rest_id}, {'$pull': {'cardapio': {'_id': prato['_id'], 'nome_prato': prato['nome_prato'], 'preco': prato['preco'], 'descricao': prato['descricao'], 'foto_prato': prato['foto_prato']}}})
                return {'resp': f'Prato <{prato["nome_prato"]}> deletado com sucesso', 'status_code': 200}
        return {'resp': f'Erro: O prato com id <{id_prato}> não está no cardapio do restaurante <{rest_id}>', 'status_code': 404}
    else:
        return {'resp': f'Erro: O restaurante <{rest_id}> não existe', 'status_code': 404}

def get_cardapio(id):
    rest = rest_find(id)
    if rest['status_code'] == 200:
        return {'resp': f'Cardapio do restaurante <{id}> encontrado com sucesso', 'cardapio': rest['restaurante']['cardapio'], 'status_code': 200}
    else:
        return {'resp': f'Erro: O restaurante <{id}> não existe', 'status_code': 404}

def adiciona_foto_prato(id, id_prato, json):
    if campos_obrigatorios(json, ['foto_prato']):
        mongo = db.restaurantes.update_one({'_id': id, 'cardapio._id': id_prato}, {'$set': {'cardapio.$.foto_prato': json['foto_prato']}})
        if mongo.raw_result.get('updatedExisting', None):
            return {'resp': f'Foto adicionadas ao prato com id <{id_prato}> com sucesso', 'status_code': 200}
        return {'resp': f'Erro: O restaurante <{id}> ou prato <{id_prato}> não existe', 'status_code': 404}
    return {'resp': f'Erro: O campo "foto_prato" é obrigatoria', 'status_code': 400}

def deleta_foto_prato(id, id_prato):
    mongo = db.restaurantes.update_one({'_id': id, 'cardapio._id': id_prato}, {'$set': {'cardapio.$.foto_prato': []}})
    if mongo.raw_result.get('updatedExisting', None):
        return {'resp': f'Foto deletada do prato <{id_prato}> com sucesso', 'status_code': 200}
    return {'resp': f'Erro: O restaurante <{id}> ou o prato <{id_prato}> não existem', 'status_code': 404}
