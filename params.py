import pymongo
from pymongo import MongoClient
url = None

dict_conns = {
              'localhost':{'conn':'mongodb://localhost:27017/'},
              'rafa':{'conn':'mongodb://alvnavra:temporal1@ds119060.mlab.com:19060/astronomy'},
              'harry':{'conn':'mongodb://harry:temporal1@ds119060.mlab.com:19060/astronomy'}
              }

user = 'rafa'
client = MongoClient(dict_conns[user]['conn'])
db = client.astronomy
