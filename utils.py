from os import listdir, getcwd
from os.path import dirname
import json

def info_mongo():
    arq = [f'{dirname(getcwd())}/{f}' for f in listdir(dirname(getcwd())) if f == 'MENU_mongodb.json'][0]
    with open(arq, "r") as file:
        data = json.load(file)
    return data

print(info_mongo())