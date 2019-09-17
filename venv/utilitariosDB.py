# -*- coding: utf-8 -*-
""" Controle deo acesso ao banco de dados."""

import pymongo

appDB="testes"

def getDb(db=appDB,hostMongo='localhost', portMongo=27017):
    client = pymongo.MongoClient(host=hostMongo, port=portMongo)
    db = client[db]
    return db

def loginUsuario(usuario):
    db = getDb(appDB)
    usuario = db['usuarios'].find_one(usuario.getJson())
    return usuario


