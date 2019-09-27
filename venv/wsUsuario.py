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

def getLoadUsuarios():
    usuarios = ""
    usuarioAtivo = current_user.get_id()

    db = utilitariosDB.getDb()
    adm = db['usuarios'].find({"_id":usuarioAtivo,"administrador":"S"})
    if adm == None:
        return "usuários não autorizado"
    else:
        usr = db['usuarios'].find().sort([("dataCadastro", pymongo.DESCENDING)])


    usuarios += ('<div class="card shadow mb-4">'
            '<div class="card-header py-3">'
              '<h6 class="m-0 font-weight-bold text-primary">Cadastro de Usuários</h6>'
            '</div>'
            '<div class="card-body">'
              '<div class="table-responsive">'
                '<table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">'
                  '<thead>'
                    '<tr>'
                      '<th>Nome</th>'
                      '<th>Email</th>'
                      '<th>Status</th>'
                      '<th>Data de Cadastro</th>'
                      '<th>Administrador</th>'
                    '</tr>'
                  '</thead>'
                  '<tbody>')

    for reg in usr:
        usuarios += ('<tr id="'+reg.get('_id','')+'">'
                      '<td>'+reg.get('nome','')+'</td>'
                      '<td>'+reg.get('email','')+'</td>'                    
                      '<td>'+reg.get('Status','')+'</td>'
                      '<td>'+reg.get('administrador','')+'</td>'
                    '</tr>')


    usuarios += ('</tbody>'
                '</table>'
              '</div>'
            '</div>'
          '</div>')

    return Markup(usuarios)
