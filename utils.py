from os import listdir, getcwd
from os.path import dirname
import json
from collections import Counter

def info_mongo():
    arq = [f'{dirname(getcwd())}/{f}' for f in listdir(dirname(getcwd())) if f == 'MENU_mongodb.json'][0]
    with open(arq, "r") as file:
        data = json.load(file)
    return data

def campos_obrigatorios(json, campos):
    vazio = True if (None in json.values() or '' in json.values()) else False
    todos_aparecem = Counter(json.keys()) == Counter(campos)
    return not vazio and todos_aparecem