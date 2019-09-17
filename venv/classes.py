from collections import namedtuple
import utilitariosDB

class Usuario:
    _id = ""
    nome = ""
    email = ""
    senha = ""
    token = ""
    liberado = ""
    agenda = ""
    dataCadastro = ""
    
    def __init__(self):
       pass

    def getJson(self):
        return vars(self)

    def salvarMongoDb(self, db, coll="usuarios"):
        db[coll].save(self.getJson())


class Evento:
    _id = None
    titulo = None
    categoria = None
    descricao = None
    momentoExecucao = None
    local = None
    pontos = None
    vagas = None
    inscricoes = None
    usuariosInscritos = None
    publicado = None
    momentoFimInscricao = None
    momentoCadastro = None

    def __init__(self):
       pass

class Post:
    _id = None
    titulo = None
    descricao = None
    midia = None
    midiaTipo = None
    comentarios = None
    curtidas = None
    momento = None

    def __init__(self):
       pass

class Comentarios:
    _id = None
    usuario = None
    post = None
    comentarioPai = None
    momento = None

    def __init__(self):
       pass