# -*- coding: utf-8 -*-
""" Controle deo acesso ao banco de dados."""

import pymongo
import json

appDB="testes"

def getDb(db=appDB,hostMongo='localhost', portMongo=27017):
    client = pymongo.MongoClient(host=hostMongo, port=portMongo)
    db = client[db]
    return db

def loginUsuario(usuario):
    db = getDb(appDB)
    qr = {}
    qr['email'] = usuario.email
    qr['senha'] = usuario.senha
    usuario = db['usuarios'].find_one(qr)
    return usuario


