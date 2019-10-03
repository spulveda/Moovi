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
                    '</tr>'
                  '</thead>'
                  '<tbody>')

    for reg in evento:
        eventos += ('<tr id="'+str(reg.get('_id'))+'" onclick="editarEvento(this)">'
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
