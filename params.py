import pymongo
from pymongo import MongoClient
url = None

dict_conns = {
              'localhost':{'conn':'mongodb://localhost:27017/'}
}

user = 'localhost'
client = MongoClient(dict_conns[user]['conn'])
db = client.flashesDB
