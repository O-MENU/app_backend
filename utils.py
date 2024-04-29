from os import listdir, getcwd
from os.path import dirname
import json, requests, urllib
import urllib.parse
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

def busca_loc(address=''):
    if type(address) == int:
        end = requests.get(f'viacep.com.br/ws/{address}/json/')
        address = end['logradouro']+end['localidade']

    link = f'https://geocode.search.hereapi.com/v1/geocode?q={urllib.parse.quote_plus(address)}&apiKey=WcO15K23iW5HkYEnLSuFq15vXjzq_f8VhHU4E66pr6E'
    val = requests.get(link)
    return json.loads(val.text)['items'][0]['position']

def calcula_dist(user_loc, rest_loc):
    api_key = 'WcO15K23iW5HkYEnLSuFq15vXjzq_f8VhHU4E66pr6E'
    if type(user_loc) == dict:
        user_loc = (user_loc['lat'], user_loc['lng'])

    if type(rest_loc) == dict:
        rest_loc = (rest_loc['lat'], rest_loc['lng'])

    url_pedestre = f'https://router.hereapi.com/v8/routes?transportMode=pedestrian&origin={user_loc[0]},{user_loc[1]}&destination={rest_loc[0]},{rest_loc[1]}&return=travelSummary&apikey={api_key}'
    dist_pedestre = requests.get(url_pedestre).json()['routes'][0]['sections'][0]['travelSummary']['length']

    url_carro = f'https://router.hereapi.com/v8/routes?transportMode=car&origin={user_loc[0]},{user_loc[1]}&destination={rest_loc[0]},{rest_loc[1]}&return=travelSummary&apikey={api_key}'
    dist_carro = requests.get(url_carro).json()['routes'][0]['sections'][0]['travelSummary']['length']

    return {'carro' : dist_carro, 'pedestre' : dist_pedestre}

print(calcula_dist(busca_loc('1901 S Atlantic Ave, Daytona Beach', 'Orlando'), busca_loc('200 Rialto PI, Melbourne', 'Orlando')))