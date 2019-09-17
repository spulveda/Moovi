""" Controle deo acesso ao banco de dados."""

import pymongo

def getDb(db,hostMongo='localhost', portMongo=27017):
    client = pymongo.MongoClient(host=hostMongo, port=portMongo)
    db = client[db]
    return db

