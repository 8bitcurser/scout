from os import environ

from pymongo import MongoClient


client = MongoClient(environ.get('ME_CONFIG_MONGODB_URL', ''))
# mongo creates it if it doesnt exist.
db = client['local']
collection = db['tokens']