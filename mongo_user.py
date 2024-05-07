import pymongo
import pprint
import statistics
from utils import *
from mongo_rest import *

client, db = conn_mongo()

counter = db.counters.find_one()
usuario_id = counter['usuarios_id']
avaliacao_id = counter['avaliacoes_id']

# cadastro de usuario
def user_add(json):
  if campos_obrigatorios(json, ['nome', 'email', 'data_aniversario', 'data_cadastro', 'senha', 'foto_perfil']):
    user = db.usuarios.find_one({'email':json['email']})
    if user == None:
      dic = {
        '_id': usuario_id,
        'nome': json['nome'],
        'email': json['email'],
        'data_aniversario': json['data_aniversario'],
        'data_cadastro': json['data_cadastro'],
        'senha': json['senha'],
        'foto_perfil': json['foto_perfil'],
        'rest_fav': [],
        'comida_fav': [],
        'seguindo': [],	
        'seguidores': [],
        'locs': [], 
      }
      db.counters.update_one({}, {'$inc':{'usuarios_id':1}})
      db.usuarios.insert_one(dic)
      return {'resp':{'message':'Usuario cadastrado com sucesso!', 'user': dic}, 'status_code': 201}
    else:
      return {'resp':'Erro: Usuario já existe!', 'status_code': 400}
  else:
    return {'resp':'Erro: Todos os campos são obrigatorios!', 'status_code': 400}

# acha usuario por id ou lista todos os usuarios
def user_find(usuario_id=None):
  if usuario_id == None:
    users = db.usuarios.find()
    return {'resp': 'Usuarios encontrados com sucesso', 'users': list(users), 'status_code': 200}
  else:
    user = db.usuarios.find_one({'_id': usuario_id})
    if user == None:
      return {'resp': f'Erro: O usuario <{usuario_id}> não existe', 'status_code': 404}
    else:
      return {'resp': f'Usuario <{usuario_id}> encontrado com sucesso', 'user': user, 'status_code': 200}

# atualiza informacoes basicas do usuario (nome, email, data de nascimento, senha)
def user_update(usuario_id, json):
  user = user_find(usuario_id)
  if user['status_code'] == 200:
    if campos_obrigatorios(json, ['nome', 'email', 'data', 'senha', 'foto_perfil']):
      for key in json.keys():
        db.usuarios.update_one({'_id': usuario_id}, {'$set': {key: json[key]}})
      return {'resp': f'Usuario <{usuario_id}> editado com sucesso', 'status_code': 200}
    else:
      return {'resp': f'Erro: O campo <{key}> não é suportado / json vazio', 'status_code': 404}
  else:
    return {'resp': f'Erro: O usuario <{usuario_id}> não existe', 'status_code': 404}

# deleta usuario pelo id
def user_delete(usuario_id):
  user = user_find(usuario_id)
  if user['status_code'] == 200:
    db.usuarios_deletados.insert_one(user['user'])
    db.usuarios.delete_one({'_id': usuario_id})
    return {'resp': f'O usuario <{usuario_id}> foi deletado com sucesso', 'status_code': 200}
  else:
    return {'resp': f'Erro: O usuario <{usuario_id}> não existe', 'status_code': 404}

# usuario 1 segue usuario 2
def user_seguir_add(usuario_id, amigo_id):
  user = user_find(usuario_id)
  amigo = user_find(amigo_id)
  if user['status_code'] == 200 and amigo['status_code'] == 200:
    user = user['user']
    amigo = amigo['user']
    for dic_amigo in user['seguindo']:
      if amigo_id == dic_amigo['_id']:
        return {'resp': f'Erro: O usuario <{usuario_id}> já segue o usuario <{amigo_id}>', 'status_code': 400}
    db.usuarios.update_one({'_id': usuario_id}, {'$push': {'seguindo': {'_id': amigo_id, 'nome': amigo['nome']}}})
    db.usuarios.update_one({'_id': amigo_id}, {'$push': {'seguidores': {'_id': usuario_id, 'nome': user['nome']}}})
    return {'resp': f'Usuario <{usuario_id}> começou a seguir o usuario <{amigo_id}>', 'status_code': 200}
  else:
    return {'resp': f'Erro: Usuario <{usuario_id}> ou <{amigo_id}> não existem', 'status_code': 404}

# usuario 1 para de seguir usuario 2
def user_seguir_delete(usuario_id, amigo_id):
  user, amigo = user_find(usuario_id), user_find(amigo_id)
  if user['status_code'] == 200 and amigo['status_code'] == 200:
    user, amigo = user['user'], amigo['user'] 
    for dic_amigo in user['seguindo']:
      if amigo_id == dic_amigo['_id']:
        db.usuarios.update_one({'_id': usuario_id}, {'$pull': {'seguindo': {'_id': amigo_id, 'nome': amigo['nome']}}})
        db.usuarios.update_one({'_id': amigo_id}, {'$pull': {'seguidores': {'_id': usuario_id, 'nome': user['nome']}}})
        return {'resp': f'O usuario <{usuario_id}> parou de seguir o usuario <{amigo_id}>', 'status_code': 200}
    return {'resp': f'Usuario <{usuario_id}> não segue o usuario <{amigo_id}>', 'status_code': 400}
  else:
    return {'resp': f'Erro: Usuario <{usuario_id}> ou usuario <{amigo_id}> não existem', 'status_code': 404}

# adiciona comida fav ao usuario. (futuramente refatorar comida para lista)
def user_comida_add(usuario_id, comidas: list):
  user = user_find(usuario_id)
  if user['status_code'] == 200:
    user = user['user']
    for comida in comidas:
      if comida not in user['comida_fav']:
        db.usuarios.update_one({'_id': usuario_id}, {'$push': {'comida_fav': comida}})
    return {'resp': f'Comidas <{comidas}> adicionadas ao usuario <{usuario_id}>', 'status_code': 200}
  else:
    return {'resp': f'Erro: O usuario <{usuario_id}> não existe', 'status_code': 404}

# retira comida da lista de favoritos do usuario 
def user_comida_delete(usuario_id, comidas: list):
  user = user_find(usuario_id)
  if user['status_code'] == 200:
    user = user['user']
    for comida in comidas:
      if comida in user['comida_fav']:
        db.usuarios.update_one({'_id': usuario_id}, {'$pull': {'comida_fav': comida}})
    return {'resp': f'Comidas <{comidas}> removidas com sucesso do usuario <{usuario_id}>', 'status_code': 200}
  else:
    return {'resp': f'Erro: O usuario <{usuario_id}> não existe', 'status_code': 404}

# adiciona restaurante fav ao perfil do usuario 
def user_rest_add(usuario_id, rest_id):
  user, rest = user_find(usuario_id), rest_find(rest_id)
  if user['status_code'] == 200 and rest['status_code'] == 200:
    user, rest = user['user'], rest['restaurante']
    for restaurante in user['rest_fav']:
      if rest_id == restaurante['_id']:
        return {'resp': f'Erro: O restaurante <{rest_id}> já esta favoritado pelo usuario <{usuario_id}>', 'status_code': 400}
    db.usuarios.update_one({'_id': usuario_id}, {'$push': {'rest_fav': {'_id': rest_id, 'nome': rest['nome']}}})
    return {'resp': f'Restaurante <{rest_id}> adicionado com sucesso aos favoritos do usuario <{usuario_id}>', 'status_code': 200}
  else:
    return {'resp': f'Erro: Usuario <{usuario_id}> ou restaurante <{rest_id}> não existe'}

# retira restaurnte fav do perfil do usuario
def user_rest_delete(usuario_id, rest_id):
  user, rest = user_find(usuario_id), rest_find(rest_id)
  if user['status_code'] == 200 and rest['status_code'] == 200:
    user, rest = user['user'], rest['restaurante']
    for rest in user['rest_fav']:
      if rest_id == rest['_id']:
        db.usuarios.update_one({'_id': usuario_id}, {'$pull': {'rest_fav': {'_id': rest_id, 'nome': rest['nome']}}})
        return {'resp': f'Restaurante <{rest_id}> removido com sucesso do usuario <{usuario_id}>', 'status_code': 200}
    return {'resp': f'Erro: O restaurante <{rest_id}> não esta na lista de favoritos do usuario <{usuario_id}>', 'status_code': 400}
  else:
    return {'resp': f'Erro: Usuario <{usuario_id}> ou restaurante <{rest_id}> não existe', 'status_code': 404}

# tipo 1) avaliacao_find(usuario_id, rest_id) => Avaliacao que o usuario x deu ao restaurante y
# tipo 2) avaliacao_find(usuario_id, _) => Lista todas as avaliacoes que o usuario x fez
# tipo 3) avaliacao_find(_, rest_id) => Lista todas as avaliacoes que o restaurante y recebeu
#tipo 4) avaliacao_find(_, _) => Lista TODAS as avaliacoes do banco de dados
def avaliacao_find(usuario_id=None, rest_id=None):
  user, rest = user_find(usuario_id), rest_find(rest_id)
  if usuario_id == None and rest_id == None:
    avaliacoes = db.avaliacoes.find()
    return {'resp': 'Avaliações listadas com sucesso', 'avaliacoes': list(avaliacoes), 'status_code': 200}
  elif usuario_id != None and rest_id == None:
    if user['status_code'] == 200:
      avaliacoes = db.avaliacoes.find({'usuario_id': {'$all': [usuario_id]}})
      avaliacoes = list(avaliacoes)
      if avaliacoes == []:
        return {'resp': f'Erro: O usuario <{usuario_id}> não fez nenhuma avaliacão', 'status_code': 400}
      else:
        return {'resp': f'Avaliações do usuario <{usuario_id}> listadas com sucesso', 'avaliacoes': avaliacoes, 'status_code': 200}
    else:
      return {'resp': f'O usuario <{usuario_id}> não existe', 'status_code': 404}
  elif usuario_id == None and rest_id != None:
    if rest['status_code'] == 200:
      avaliacoes = db.avaliacoes.find({'restaurante_id': {'$all': [rest_id]}})
      avaliacoes = list(avaliacoes)
      if avaliacoes == []:
        return {'resp': f'Erro: O restaurante <{rest_id}> não tem nenhuma avaliacão', 'status_code': 400}
      else:
        return {'resp': f'Avaliações do restaurante <{rest_id}> listadas com sucesso', 'avaliacoes': avaliacoes, 'status_code': 200}
    else:
      return {'resp': f'O restaurante <{rest_id}> não existe', 'status_code': 404}
  else:
    if user['status_code'] == 200 and rest['status_code'] == 200:
      avaliacao = db.avaliacoes.find_one({'usuario_id': usuario_id, 'restaurante_id': rest_id})
      if avaliacao == None:
        return {'resp': f'Erro: O usuario <{usuario_id}> não fez nenhuma avaliação do restaurante <{rest_id}>', 'status_code': 400}
      else:
        return {'resp': f'Avaliação do usuario <{usuario_id}> do restaurante <{rest_id}>', 'avaliacao': avaliacao, 'status_code': 200}    
    else:
      return {'resp': f'Erro: O usuario <{usuario_id}> ou o restaurante <{rest_id}> não existem', 'status_code': 404}
# adiciona uma avaliacao do usuario x ao restaurante y, recebe (usuario_id; rest_id; nota de 0 a 5; "pontos_fortes" é como, 'o que podemos melhorar', uma lista de avaliacoes pre definidas como = [sabor, tempero, quantidade, temperatura, prato errado]; comentario sobre o restaurante)
def user_avaliacao_add(usuario_id, rest_id, json): # nota pontos_fortes comentario
  user, rest, avaliacao= user_find(usuario_id), rest_find(rest_id), avaliacao_find(usuario_id, rest_id)
  if user['status_code'] == 200 and rest['status_code'] == 200:
    user, rest = user['user'], rest['restaurante']
    if avaliacao['status_code'] == 400:
      dic = {
        '_id': avaliacao_id,
        'restaurante_id': rest_id,
        'usuario_id': usuario_id,
      }

      for key in json.keys():
        dic[key] = json[key]
      db.avaliacoes.insert_one(dic)
      db.counters.update_one({}, {'$inc': {'avaliacoes_id': 1}})
    else:
      dic = {}
      for key in json.keys():
        dic[key] = json[key]
      db.avaliacoes.update_one({'_id': avaliacao['avaliacao']['_id']}, {'$unset': {'avaliacao.nota': 1, 'avaliacao.pontos_fortes': 1, 'avaliacao.comentario': 1}})
      db.avaliacoes.update_one({'_id': avaliacao['avaliacao']['_id']}, {'$set': dic})
    avaliacoes = avaliacao_find(None, rest_id)
    notas = []
    if len(avaliacoes) > 0:
      for ava in avaliacoes['avaliacoes']:
        notas.append(ava['nota'])
      nota_rest = statistics.mean(notas)
      db.restaurantes.update_one({'_id': rest_id}, {'$set': {'nota': float(f'{nota_rest:.1f}')}})
    else:
      if 'nota' in json.keys():
        nota_rest = json['nota']
        db.restaurantes.update_one({'_id': rest_id}, {'$set': {'nota': float(f'{nota_rest:.1f}')}})
    return {'resp': f'Usuario <{usuario_id}> avaliou o restaurante <{rest_id}>', 'status_code': 200}
  else:
    return {'resp': f'Erro: Usuario <{usuario_id}> ou restaurante <{rest_id}> não existe', 'status_code': 404}

def locs_usuario(usuario_id):
  user = user_find(usuario_id)
  if user['status_code'] == 200:
    return {'resp': user['user']['locs'], 'status_code': 200}
  return {'resp': f'Erro: Usuario <{usuario_id}> não existe', 'status_code': 404}

def locs_usuarios():
  loc = []
  all_locs = db.usuarios.find({}, {'locs': 1, '_id': 0})
  for locs in all_locs:
    for ltlng in locs['locs']:
      loc.append(ltlng)
  return {'resp': 'Localizações dos usuarios listadas', 'locs': loc, 'status_code': 200}

def loc_usuario_add(usuario_id, loc):
  user = user_find(usuario_id)
  if user['status_code'] == 200:
    ltlng = loc['loc']
    db.usuarios.update_one({'_id': usuario_id}, {'$push': {'locs': ltlng}})
    return {'resp': f'Localização adicionada com sucesso ao usuario <{usuario_id}>', 'status_code': 200}
  return {'resp': f'Erro: Usuario <{usuario_id}> não existe', 'status_code': 404}


#############FUNCAO REST POR CONTA DE CIRCULAR IMPORT###########################################################


def rest_possiveis_clientes(rest_id):
  possiveis_clientes = []
  rest = rest_find(rest_id)
  if rest == None:
    return {'resp': f'Erro: O restaurante <{rest_id}> não foi encontrado', 'status_code': 404}
  preferencias = rest['restaurante']['categorias']
  usuarios = user_find()
  for user in usuarios['users']:
    for categoria in preferencias:
      if  categoria in user['comida_fav']:
        if user not in possiveis_clientes:
          possiveis_clientes.append(user)
  if len(possiveis_clientes) == 0:
    return {'resp': f'Erro: Nenhum possivel cliente encontrado para o restaurante <{rest_id}>', 'status_code': 404}
  return {'resp': f'Possiveis clientes do restaurante <{rest_id}> encontrados com sucesso', 'possiveis_clientes': possiveis_clientes, 'status_code': 200}

