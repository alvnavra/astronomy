import pymongo
from pymongo import MongoClient
url = None
client = MongoClient('mongodb://localhost:27017/')
db = client.flashes
