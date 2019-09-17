from collections import namedtuple

class Usuario(object):
    usuarioId = None
    nome = None
    email = None
    senha = None
    token = None
    liberado = None
    agenda = None
    dataCadastro = None
    
    def __init__(self):
        pass

def iniciarUsuario(dados):
    return namedtuple("Usuario", dados.keys())(*dados.values())

            


class Evento(object):
    eventoId = None
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


class Post(object):
    postId = None
    titulo = None
    descricao = None
    midia = None
    midiaTipo = None
    comentarios = None
    curtidas = None
    momento = None


class Comentarios(object):
    comentarioId = None
    usuario = None
    post = None
    comentarioPai = None
    momento = None