# -*- coding: utf-8 -*-
from collections import namedtuple
import utilitariosDB
from flask_login import UserMixin

class Usuario(UserMixin):
    _id = ""
    nome = ""
    email = ""
    senha = ""
    token = ""
    liberado = ""
    agenda = ""
    dataCadastro = ""
    imagem = ""
    administrador = ""
    
    def __init__(self,_id="",nome = "",email = "",senha = "",token = "",liberado = "",agenda = "",dataCadastro = "", imagem = "", administrador = ""):
        self._id = _id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.token = token
        self.liberado = liberado
        self.agenda = agenda
        self.dataCadastro = dataCadastro
        self.imagem = imagem
        self.administrador = administrador

    def getJson(self):
        return vars(self)

    def salvarMongoDb(self, db, coll="usuarios"):
        dados = self.getJson()
        del dados["_id"]
        db[coll].save(dados)

    def fromJson(self,json):
        d = dict(json)
        for k, v in d.items():
            setattr(self, k, v)

    def get_id(self):
        return str(self._id)

class Evento:
    _id = None
    titulo = None
    categoria = None
    descricao = None
    imagem = None
    momentoExecucao = None
    local = None
    pontos = None
    vagas = None
    inscricoes = None
    usuariosInscritos = None
    publicado = None
    momentoFimInscricao = None
    momentoCadastro = None
    concluido = None
    feedBackTipo = None
    usuariosFeedBack = None
    usuariosFeedBackOk = None

    def __init__(self):
       pass

    def getJson(self):
        return vars(self)

    def salvarMongoDb(self, db, coll="evento"):
        db[coll].save(self.getJson())

    def fromJson(self,json):
        d = dict(json)
        for k, v in d.items():
            setattr(self, k, v)

class EventoFeedBack(object):
    _id = None
    feedBackTipo = None
    feedBack = None
    evento = Evento
    usuario = Usuario
    status = None

    def __init__(self):
       pass

    def getJson(self):
        return vars(self)

    def salvarMongoDb(self, db, coll="eventoFeedBack"):
        db[coll].save(self.getJson())

    def fromJson(self,json):
        d = dict(json)
        for k, v in d.items():
            setattr(self, k, v)

class Post:
    _id = None
    titulo = None
    descricao = None
    midia = None
    midiaTipo = None
    comentarios = None
    curtidas = None
    momento = None
    eventos = None

    def __init__(self):
       pass

    def getJson(self):
        return vars(self)

    def salvarMongoDb(self, db, coll="post"):
        db[coll].save(self.getJson())

    def fromJson(self,json):
        d = dict(json)
        for k, v in d.items():
            setattr(self, k, v)

class Comentarios:
    _id = None
    usuario = None
    post = None
    comentario = None
    momento = None

    def __init__(self):
       pass

    def getJson(self):
        return vars(self)

    def salvarMongoDb(self, db, coll="comentarios"):
        db[coll].save(self.getJson())

    def fromJson(self,json):
        d = dict(json)
        for k, v in d.items():
            setattr(self, k, v)
