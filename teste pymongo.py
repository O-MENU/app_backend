import pymongo
from datetime import date
from details import psswd, user

mongo_app = 'fotosWebapp'
mongo_conn = f'mongodb+srv://{user}:{psswd}@{mongo_app.lower()}.3pocv7k.mongodb.net/?retryWrites=true&w=majority&appName={mongo_app}'
client = pymongo.MongoClient(mongo_conn)

database = client['fotosWebapp']
collection = database['eventos']

doc = {
     "_id" : 2,
     "media": {
          "url": "https://youtube.com/2aaaaaaaaaaaaaaaaaaaaaaa2",
          "caption": "whoops, I did it again"
        },
        "start_date": {
          "year" : "2939",
          "month" : "5",
          "day" : "6"
        },
        "text": {
          "headline": "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK",
          "text": ""
}
}

#x = collection.insert_one(doc)
#print('ok')

for x in collection.find():
    del x['_id']
    print(date(year = int(x['start_date']['year']), month=int(x['start_date']['month']), day=int(x['start_date']['day'])))
    print('--------------')