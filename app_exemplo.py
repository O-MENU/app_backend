from flask import Flask, request, jsonify
import json
import pandas as pd
from datetime import date

app = Flask("MENU")

conn = """Conexão com MongoDB"""

#--------------------------- Root ----------------------------

#GET (/): Deve retornar "Hello, World!".
@app.route("/", methods=["GET"])
def hello_world():
    return "Hello, World!"
#-----------------------------------------------------------------

#--------------------------- Livros ----------------------------

#GET (/livro): Lista todos os livros. Suporte para query por gênero.
@app.route("/livro", methods=["GET"])
def get_livros():
    cur = conn.cursor()
    args = request.args.to_dict()

    try:
        if args:
            cur.execute(f"SELECT * FROM livros WHERE genero = %(genero)s", args)
        else:
            cur.execute("SELECT * FROM livros")
        data = cur.fetchall()
    except psycopg2.Error as e:
        return {"erro": str(e)}, 400
    finally:
        cur.close()

    return {"livros" : data}, 200
#-----------------------------------------------------------------
    
#POST (/livro): Cadastro de um novo livro.
@app.route("/livro", methods=["POST"])
def post_livro():
    cur = conn.cursor()
    dic_livro = request.json

    for key in ["titulo", "autor", "ano_publi", "genero"]:
        if key not in dic_livro.keys():
            if key == "titulo":
                return {"message" : "Necessário informar Título do livro."}, 400
            elif key == "ano_publi":
                dic_livro[key] = 0
            else:
                dic_livro[key] = ""

    try:
        cur.execute("""INSERT INTO livros (titulo, autor, ano_publi, genero) 
                    VALUES ('{titulo}', '{autor}', {ano_publi}, '{genero}')""".format(**dic_livro))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return {"erro": str(e)}, 400
    finally:
        cur.close()

    resp = {
    "message": "Livro cadastrado",
    "livro": dic_livro}

    return resp, 201
#-----------------------------------------------------------------

#GET (/livro/<int:id>): Retorna detalhes de um livro específico pelo ID.
@app.route("/livro/<int:id>", methods=["GET"])
def get_livro(id):
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT * FROM livros WHERE id={id}")
        data = cur.fetchone()
    except psycopg2.Error as e:
        return {"erro": str(e)}, 400
    finally:
        cur.close()

    if data == None:
        return {'message' : f'Livro com ID={id} não encontrado.'}, 204
    else:
        return {"livro" : data}, 200
#-----------------------------------------------------------------

#DELETE (/livro/<int:id>): Exclui um livro pelo ID.
@app.route("/livro/<int:id>", methods=["DELETE"])
def delete_livro(id):
    cur = conn.cursor()
    try:
        cur.execute(f"DELETE FROM livros WHERE id={id}")
        if cur.rowcount == 0:
            return {"message" : f"Livro com ID={id} não existe."}, 204
        else:
            conn.commit()
            return {"message" : f"Livro com ID={id} deletado com sucesso."}, 200
    except psycopg2.Error as e:
        conn.rollback()
        return {"erro": str(e)}, 400
    finally:
        cur.close()
#-----------------------------------------------------------------

#PUT (/livro/<int:id>): Atualiza um livro pelo ID.
@app.route("/livro/<int:id>", methods=["PUT"])
def update_livro(id):
    cur = conn.cursor()
    dic_livro = request.json
    try:
        cur.execute(f"SELECT * FROM livros WHERE id={id}")
        if cur.rowcount == 0:
            return {"message" : f"Livro com ID={id} não existe."}, 204
        else:
            values = cur.fetchone()
            cols = ['titulo', 'autor', 'ano_publi', 'genero']
            values = dict([(cols[i], values[i+1]) for i in range(len(values)-1)])
            
            for k, val in dic_livro.items():
                values[k] = val
            
            values = [f'{cols[i]} = \'{values[cols[i]]}\'' if cols[i] != 'ano_publi' else f'{cols[i]} = {values[cols[i]]}' for i in range(len(cols))]
            cur.execute(f'UPDATE livros SET {", ".join(values)} WHERE id={id}')
            conn.commit()
            return {'message' : f'Livro com ID={id} atualizado com sucesso.'}, 200

    except psycopg2.Error as e:
        conn.rollback()
        return {"erro": str(e)}, 400
    finally:
        cur.close()
#-----------------------------------------------------------------
    
#--------------------------- Usuários ----------------------------
    
#GET (/usuario): Lista todos os usuários.
@app.route("/usuario", methods=["GET"])
def get_usuarios():
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM usuarios")
    except psycopg2.Error as e:
        return {"erro": str(e)}, 400
    finally:
        data = cur.fetchall()
        cur.close()

    return {"usuarios" : data}, 200
#-----------------------------------------------------------------
    
#POST (/usuario): Cadastro de um novo usuário.
@app.route("/usuario", methods=["POST"])
def post_usuario():
    cur = conn.cursor()
    dic_user = request.json

    for key in ["nome", "email", "data_cadastro"]:
        if key not in dic_user.keys():
            if key == "nome":
                return {"message" : "Necessário informar Nome do usuário."}, 400
            elif key == "data_cadastro":
                dic_user[key] = date.today()
            else:
                dic_user[key] = ""

    try:
        cur.execute("""INSERT INTO usuarios (nome, email, data_cadastro) 
                    VALUES('{nome}', '{email}', '{data_cadastro}')""".format(**dic_user))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return {"erro": str(e)}, 400
    finally:
        cur.close()

    resp = {
    "message": "Usuário cadastrado",
    "usuario": dic_user}

    return resp, 201
#-----------------------------------------------------------------

#GET (/usuario/<int:id>): Retorna detalhes de um usuário específico pelo ID.
@app.route("/usuario/<int:id>", methods=["GET"])
def get_usuario(id):
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT * FROM usuarios WHERE id={id}")
    except psycopg2.Error as e:
        return {"erro": str(e)}, 400
    finally:
        data = cur.fetchone()
        cur.close()

    return {"usuario" : data}, 200
#-----------------------------------------------------------------

#DELETE /usuario/<int:id>: Exclui um usuário pelo ID.
@app.route("/usuario/<int:id>", methods=["DELETE"])
def delete_usuario(id):
    cur = conn.cursor()
    try:
        cur.execute(f"DELETE FROM usuarios WHERE id={id}")
        if cur.rowcount == 0:
            return {"message" : f"Usuário com ID={id} não existe."}, 204
        else:
            conn.commit()
            return jsonify({"message" : f"Usuário com ID={id} deletado com sucesso."}), 200
    except psycopg2.Error as e:
        conn.rollback()
        return {"erro": str(e)}, 400
    finally:
        cur.close()
#-----------------------------------------------------------------

#PUT (/usuario/<int:id>): Atualiza um usuário pelo ID.
@app.route("/usuario/<int:id>", methods=["PUT"])
def update_usuario(id):
    cur = conn.cursor()
    dic_livro = request.json
    try:
        cur.execute(f"SELECT * FROM usuarios WHERE id={id}")
        if cur.rowcount == 0:
            return {"message" : f"Usuário com ID={id} não existe."}, 204
        else:
            values = cur.fetchone()
            cols = ["nome", "email", "data_cadastro"]
            values = dict([(cols[i], values[i+1]) for i in range(len(values)-1)])
            
            for k, val in dic_livro.items():
                values[k] = val
            
            values = [f'{cols[i]} = \'{values[cols[i]]}\'' for i in range(len(cols))]
            cur.execute(f'UPDATE usuarios SET {", ".join(values)} WHERE id={id}')
            conn.commit()
            return {'message' : f'Usuário com ID={id} atualizado com sucesso.'}, 200

    except psycopg2.Error as e:
        conn.rollback()
        return {"erro": str(e)}, 400
    finally:
        cur.close()

if __name__ == "__main__":
    app.run(debug=True)
