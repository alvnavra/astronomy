from pymongo import MongoClient
url = None
client = MongoClient('mongodb://harry:temporal1@ds119060.mlab.com:19060/astronomy')
db = client.astronomy
