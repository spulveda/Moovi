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
              '<h6 class="m-0 font-weight-bold text-primary">Administração de Usuários</h6>'
            '</div>'
            '<div class="card-body">'
              '<div class="table-responsive">'
                '<table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">'
                  '<thead>'
                    '<tr>'
                      '<th>Nome</th>'
                      '<th>Email</th>'
                      '<th>Liberado</th>'
                      '<th>Data de Cadastro</th>'
                      '<th>Administrador</th>'
                    '</tr>'
                  '</thead>'
                  '<tbody>')

    for reg in usr:
        usuarios += ('<tr id="'+str(reg.get('_id'))+'" onclick="editarUsuario(this)">'
                      '<td>'+reg.get('nome','')+'</td>'
                      '<td>'+reg.get('email','')+'</td>'                    
                      '<td>'+reg.get('liberado','')+'</td>'
                      '<td>'+reg.get('dataCadastro','')+'</td>'
                      '<td>'+reg.get('administrador','')+'</td>'
                    '</tr>')


    usuarios += ('</tbody>'
                        '</table>'
                      '</div>'
                    '</div>'
                  '</div>')

    return render_template("admUsuario.html", contentWS=Markup(usuarios))

def liberarUsuario(usuario):
    usuarioAtivo = current_user.get_id()

    db = utilitariosDB.getDb()
    adm = db['usuarios'].find({"_id": usuarioAtivo, "administrador": "S"})
    if adm == None:
        return "usuários não autorizado"
    else:
        usr = db['usuarios'].find_one({"_id":ObjectId(usuario)})
        if usr != None:
            if usr.get('liberado','') == "S":
                usr['liberado'] = "N"
            else:
                usr['liberado'] = "S"
            db['usuarios'].save(usr)

        ret = Markup(
                      '<td>'+usr.get('nome','')+'</td>'
                      '<td>'+usr.get('email','')+'</td>'                    
                      '<td>'+usr.get('liberado','')+'</td>'
                      '<td>'+usr.get('dataCadastro','')+'</td>'
                      '<td>'+usr.get('administrador','')+'</td>'
                  )
        return ret