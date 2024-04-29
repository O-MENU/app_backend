from os import listdir, getcwd
from os.path import dirname
import json, requests, urllib
from collections import Counter
import pymongo
from geopy.distance import geodesic

def info_mongo():
    arq = [f'{dirname(getcwd())}/{f}' for f in listdir(dirname(getcwd())) if f == 'MENU_mongodb.json'][0]
    with open(arq, "r") as file:
        data = json.load(file)
    return data

def campos_obrigatorios(json, campos):
    vazio = True if (None in json.values() or '' in json.values()) else False
    todos_aparecem = Counter(json.keys()) == Counter(campos)
    return not vazio and todos_aparecem

def conn_mongo():
    client = pymongo.MongoClient('mongodb+srv://henriquebrnetto02:2K4y7AIS4IOddUkC@menu.cyvtolc.mongodb.net/?retryWrites=true&w=majority&appName=MENU')
    return client, client['MENU']

def busca_loc(address):
    link = 'https://geocode.search.hereapi.com/v1/geocode?q=' + urllib.parse.quote_plus(address) + '+Sao+Paulo&apiKey=WcO15K23iW5HkYEnLSuFq15vXjzq_f8VhHU4E66pr6E'
    val = requests.get(link)
    return json.loads(val.text)['items'][0]['position']

def calcula_dist(user_loc, rest_loc):
    api_key = 'WcO15K23iW5HkYEnLSuFq15vXjzq_f8VhHU4E66pr6E'
    if type(user_loc) == dict:
        user_loc = (user_loc['lat'], user_loc['lng'])

    if type(rest_loc) == dict:
        rest_loc = (rest_loc['lat'], rest_loc['lng'])

    url = f'https://router.hereapi.com/v8/routes?transportMode=car&origin={user_loc[0]},{user_loc[1]}&destination={rest_loc[0]},{rest_loc[1]}&return=travelSummary,polyline&spans=streetAttributes,length,segmentRef&apikey={api_key}'
    return requests.get(url).json()

print(calcula_dist(busca_loc('Rua Dr. Renato Paes de Barros 283'), busca_loc('R. Pedroso Alvarenga, 365')))


