# -*- coding: utf-8 -*-
import appPadrao
from flask_login import UserMixin, current_user
from classes import Usuario, Evento
from flask import *
from flask_login import LoginManager, login_required, login_user, logout_user
import utilitariosDB
from datetime import datetime
import pymongo
from bson.objectid import ObjectId
from utils import getSideBar, getNavBar


def getLoadAtividades():
    eventos = ""
    usuarioAtivo = current_user.get_id()

    db = utilitariosDB.getDb()
    adm = db['usuarios'].find({"_id":usuarioAtivo,"administrador":"S"})
    if adm == None:
        return "usuários não autorizado"
    else:
        evento = db['evento'].find().sort([("dataCadastro", pymongo.DESCENDING)])

    eventos += ('<div class="card shadow mb-4">'
            '<div class="card-header py-3">'
              '<h6 class="m-0 font-weight-bold text-primary">Administração de Usuários</h6>'
                '<a href="/cadadmatividades">'
                    '<button type="button" class="btn btn-primary float-right" >Cadastrar</button>'
                '</a>'
            '</div>'
            '<div class="card-body">'
              '<div class="table-responsive">'
                '<table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">'
                  '<thead>'
                    '<tr>'
                      '<th>Titulo</th>'
                      '<th>Categoria</th>'
                      '<th>Execução</th>'
                      '<th>Local</th>'
                      '<th>Pontos</th>'
                      '<th>Vagas</th>'
                      '<th>Inscrições</th>'
                      '<th>Publicado</th>'
                      '<th>Concluído</th>'
                      '<th>Cadastro</th>'
                      '<th>Publicar</th>'
                      '<th>Concluir</th>'  
                    '</tr>'
                  '</thead>'
                  '<tbody>')

    for reg in evento:
        eventos += ('<tr id="'+str(reg.get('_id'))+'">'
                      '<td>'+reg.get('titulo','')+'</td>'
                      '<td>'+reg.get('categoria','')+'</td>'                    
                      '<td>'+reg.get('momentoExecucao','').strftime("%d/%m/%y")+'</td>'
                      '<td>'+reg.get('local','')+'</td>'
                      '<td>'+str(reg.get('pontos',''))+'</td>'
                      '<td>'+str(reg.get('vagas',''))+'</td>'
                      '<td>'+str(reg.get('inscricoes',''))+'</td>'
                      '<td>'+reg.get('publicado','')+'</td>'
                      '<td>'+reg.get('concluido','')+'</td>'
                      '<td>'+reg.get('momentoCadastro','').strftime("%d/%m/%y")+'</td>'
                      '<td> <button type="button" class="btn btn-primary" onclick="publicarEvento(this)">Publicar</button></td>'
                      '<td><button type="button" class="btn btn-primary" onclick="concluirEvento(this)">Concluir</button></td>'
                                                                               
                    '</tr>')

    eventos += ('</tbody>'
                        '</table>'
                      '</div>'
                    '</div>'
                  '</div>')

    sideBar = Markup(getSideBar())

    usuario = db['usuarios'].find_one({"_id": ObjectId(usuarioAtivo)})
    navbar = Markup(getNavBar(usuario))

    return render_template("admUsuario.html", contentWS=Markup(eventos), sideBarWS=sideBar, navbarWS=navbar)


def cadAdmAtividades():
    if request.method == 'GET':
        usuarioAtivo = current_user.get_id()

        db = utilitariosDB.getDb()
        sideBar = Markup(getSideBar())

        usuario = db['usuarios'].find_one({"_id": ObjectId(usuarioAtivo), "administrador": "S"})
        if usuario == None:
            return "usuários não autorizado"

        navbar = Markup(getNavBar(usuario))

        return render_template("cadastarAtividadesDesktop.html", sideBarWS=sideBar, navbarWS=navbar)

    if request.method == 'POST':
        evento = Evento()

        evento.titulo = request.form.get("tTitulo", '')
        evento.categoria = request.form.get("selCategoria", '')
        evento.feedBackTipo = request.form.get("selFeedBack", '')
        evento.descricao = request.form.get("tDescricao", '')
        evento.imagem = request.form.get("fileBase64", '')
        evento.momentoExecucao = request.form.get("tDataEvento", None)
        evento.local = request.form.get("tLocal", '')
        evento.pontos = int(request.form.get("tPontos", 0))
        evento.vagas = int(request.form.get("tVagas", 0))
        evento.inscricoes = 0
        evento.usuariosInscritos = []
        evento.publicado = "N"
        evento.momentoFimInscricao = request.form.get("tDataFimInscricao", None)
        evento.momentoCadastro = datetime.now()
        evento.concluido = "N"

        if not evento.momentoExecucao == None:
            evento.momentoExecucao = datetime.strptime(evento.momentoExecucao, "%Y/%m/%d %H:%M")

        if not evento.momentoFimInscricao == None:
            evento.momentoFimInscricao = datetime.strptime(evento.momentoFimInscricao, "%Y/%m/%d %H:%M")

        # Salvando no banco
        db = utilitariosDB.getDb()
        evento.salvarMongoDb(db)

        return redirect('/atividades')

def getAdmFeedBack():
    # trazer todos os eventos ativos com feedback removendo os que estão no feedback ok
    # ter a intereção de dar feedback ok ou não ok
    # caso não ok o usuário deve receber um novo item na agenda

    usuarioAtivo = current_user.get_id()
    db = utilitariosDB.getDb()
    sideBar = Markup(getSideBar())

    usuario = db['usuarios'].find_one({"_id": ObjectId(usuarioAtivo), "administrador": "S"})
    if usuario == None:
        return "usuários não autorizado"

    navbar = Markup(getNavBar(usuario))

    eventoFeedBack = db['eventoFeedBack'].find({"status": "novo"})

    evento = ''
    for reg in eventoFeedBack:
        eventoDados = reg.get('evento','')
        usuarioDados = reg.get('usuario','')

        evento += ('<div  class="col-xl-12 col-md-6 mb-4">'
                   '<div class="card border-left-primary shadow h-100 py-2">'
                   '<div class="card-body">'
                   '<div class="row no-gutters align-items-center">'
                   '<div class="col mr-2">'
                   '<div class="text-xs font-weight-bold text-primary text-uppercase mb-0">' + eventoDados.get('categoria','') + ' - ' + usuarioDados.get('nome','') + '</div>'
                   '<div class="h5 mb-0 font-weight-bold text-gray-800"> Execução da atividade: ' + eventoDados.get('momentoExecucao','').strftime("%d/%m as %H horas") + '</div>'
                       '</div>'
                       '<div class="col-auto">'
                       '<i class="fas fa-calendar fa-2x text-primary mr-1" data-toggle="modal" data-target="#eventoModal' + str(reg.get('_id','')) + '"></i>'
                       '<i class="fas fa-exclamation-circle fa-2x text-danger mr-1" id="' + str(reg.get('_id','')) + '" onclick="reprovarFeedBack(this)"></i>'
                       '<i class="fas fa-check fa-2x text-success" id="' + str(reg.get('_id','')) + '" onclick="aprovarFeedBack(this)"></i>'
                        '</div>'
                        '</div>'
                        '</div>'
                        '</div>'
                        '</div>')

        evento += ('<div class="modal fade" id="eventoModal' + str(reg.get('_id','')) + '" tabindex="-1" role="dialog"  >'
                                                                               '<div class="modal-dialog" role="document">'
                                                                               '<div class="modal-content">')

        evento += ('<div class="card shadow-lg mb-4">'
                   '<div class="card-header py-3">'
                   '<h6 class="m-0 font-weight-bold text-primary text-center">' + eventoDados.get('titulo','') + '</h6>')

        evento += ('</div>'
                   '<div class="card-body pb-2 mb-1">')

        if (reg.get('feedBackTipo','') == 'TEXTO'):
            texto = reg.get('feedback','').split('\n')
            evento += ('<div class="card py-3 border-bottom-primary">'
                       '<div class="card-body pb-0 pt-0">'
                       '<p class="mb-0 pb-0 mt-0">' + str(texto) + '</p>'
                      '</div>'
                      '</div>'
                      '</div>'
                      '<div class="card-footer pb-0 pt-3 mt-0 text-center">')


        evento += ('<div class="modal-footer">'
                   '<button type="button" class="btn btn-secondary" data-dismiss="modal">Fechar</button>'
                   '</div>'
                   '</div>'
                   '</div>'
                   '</div>')


    return render_template("admFeedBack.html", contentWS=Markup(evento), sideBarWS=sideBar, navbarWS=navbar)