#create user
import pymongo

client = pymongo.MongoClient('mongodb+srv://henriquebrnetto02:2K4y7AIS4IOddUkC@menu.cyvtolc.mongodb.net/?retryWrites=true&w=majority&appName=MENU')

db = client['MENU']
counter = db.counters.find_one()
usuario_id = counter['usuarios_id']

def user_add(nome, email, data, senha):
  if nome and email and data and senha:
    user = db.usuarios.find_one({'email':email})
    if user == None:
      dic = {
        'id': usuario_id,
        'nome': nome,
        'email': email,
        'data': data,
        'senha': senha
      }
      db.counters.update_one({}, {'$inc':{'usuarios_id':1}})
      db.usuarios.insert_one(dic)
      return {'resp':'Usuario cadastrado com sucesso!', 'status_code': 201}
    return {'resp':'Erro: Usuario já existe!', 'status_code': 400}
  else:
    return {'resp':'Erro: Todos os campos são obrigatorios!', 'status_code': 400}
