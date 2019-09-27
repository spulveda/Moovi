import appPadrao
from flask_login import UserMixin, current_user
from classes import Usuario, Evento
from flask import *
from flask_login import LoginManager, login_required, login_user, logout_user
import utilitariosDB
from datetime import datetime
import pymongo
from bson.objectid import ObjectId

app = appPadrao.criar_appPadrao()


@app.route('/evento', methods=['GET'])
@login_required
def evento():

    return render_template('evento.html')

@app.route('/getEvento', methods=['GET'])
@login_required
def getEvento():
    usuarioAtivo = current_user.get_id()

    db = utilitariosDB.getDb()
    adm = db['usuarios'].find({"_id":usuarioAtivo,"administrador":"S"})
    if adm == None:
        eventos = db['evento'].find({"concluido":"N","publicado":"S"}).sort([("momentoCadastro", pymongo.DESCENDING)])
    else:
        eventos = db['evento'].find({"concluido":"N"}).sort([("momentoCadastro", pymongo.DESCENDING)])

    evento = ''
    for reg in eventos:
        eventoId = reg.get('_id','')
        titulo = reg.get('titulo', '')
        categoria = reg.get('categoria', '')
        descricao = reg.get('descricao', '')
        imagem = reg.get('imagem', '')
        momentoExecucao = reg.get('momentoExecucao', '')
        local = reg.get('local', '')
        pontos = reg.get('pontos', '')
        vagas = reg.get('vagas', '')
        inscricoes = reg.get('inscricoes', '')
        usuariosInscritos = reg.get('usuariosInscritos', None)
        publicado = reg.get('publicado', '')
        momentoFimInscricao = reg.get('momentoFimInscricao', '')
        momentoCadastro = reg.get('momentoCadastro', '')
        concluido = reg.get('concluido', '')

        descricao = "<br />".join(descricao.split("\n"))

        evento += ('<div class="card shadow-lg mb-4">'
                '<div class="card-header py-3">'
                  '<h6 class="m-0 font-weight-bold text-primary text-center">'+titulo+'</h6>')
                                                                                      

        if not adm == None:
            evento += ('<div class="dropdown no-arrow float-right">'
                        '<a class="dropdown-toggle" href="#" role="button" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
                          '<i class="fas fa-ellipsis-v fa-sm fa-fw text-gray-400"></i>'
                        '</a>'
                        '<div class="dropdown-menu dropdown-menu-right shadow animated--fade-in" aria-labelledby="dropdownMenuLink">'
                          '<div class="dropdown-header">Menu de administrador:</div>'
                          '<a class="dropdown-item" id="'+str(eventoId)+'" onclick="publicar(this)">Publico='+publicado+'</a>'
                          '<a class="dropdown-item" id="'+str(eventoId)+'" onclick="concluir(this)">Concluido='+concluido+'</a>'
                        '</div>'
                      '</div>')

        evento += ('</div>'
                '<div class="card-body pb-2 mb-1">')
        if (imagem > ''):
            evento += ('<div class="text-center ">'
                    '<img class="img-fluid px-3 px-sm-4 mt-3 mb-4 " style="width: 25rem;" src="'+imagem+'" alt="">'
                  '</div>')

        evento += ('<div class="card py-3 border-bottom-primary">'
                    '<div class="card-body pb-0 pt-0">'
                      '<p class="mb-0 pb-0 mt-0">'+descricao+'</p>'
                    '</div>'
                  '</div>'                  
                '</div>'
                '<div class="card-footer pb-0 pt-3 mt-0 text-center">'
                    
                    '<div class="btn-group mb-0" role="group">'
                      '<p  class="btn btn-success btn-icon-split">'
                        '<span class="icon text-white-50">'
                          +str(pontos)+
                        '</span>'
                        '<span class="text">Pontos</span>'
                      '</p>')
                          
        if (vagas > 0):
            evento += ('<p  class="btn btn-warning btn-icon-split ml-1">'
                        '<span class="icon text-white-50">'
                          +str(vagas-inscricoes)+
                        '</span>'
                        '<span class="text">Vagas</span>'
                      '</p>')

        evento += ('<p  class="btn btn-primary btn-icon-split ml-1">'
                        '<span class="icon text-white-50">'
                          +momentoExecucao.strftime("%d/%m")+
                        '</span>'
                        '<span class="text">'+momentoExecucao.strftime("%H")+'h</span>'
                      '</p>'                        
                    '</div>'
                    
                    '<div class="mt-0">')
        if (vagas > 0):
            evento += ('<p  class="btn btn-primary btn-icon-split ml-1">'
                        '<span class="icon text-white-50">'
                          'Incrições até'
                        '</span>'
                        '<span class="text">'+momentoFimInscricao.strftime("%d/%m")+'</span>'
                      '</p>')

        if (vagas > 0):

            if (usuariosInscritos != None) and (usuarioAtivo in usuariosInscritos):
                evento += ('<p  class="btn btn-success btn-icon-split ml-1" id="' + str(eventoId) + '" onclick="postInscreverse(this)" >'
                           '<span class="text">Inscrito</span>')
            else:
                evento += ('<p  class="btn btn-danger btn-icon-split ml-1" id="' + str(eventoId) + '" onclick="postInscreverse(this)" >'
                           '<span class="text">Inscrever-se</span>')

        evento += ('</p>'     
                        
                    '</div>'                    
                '</div>'
            '</div>')

    return Markup(evento)

@app.route('/postInscreverse',methods=["POST"])
@login_required
def postInscreverse():

    cont = json.loads(request.data.decode('utf-8'))
    eventoId = cont.get('eventoId','')
    usuario = current_user.get_id()

    db = utilitariosDB.getDb()
    evento = db['evento'].find_one({"_id":ObjectId(eventoId)})
    momentoFimInscricao = evento.get('momentoFimInscricao', None)
    inscritos = evento.get("usuariosInscritos",None)

    if (inscritos == None):
        inscritos = [usuario]
        evento["usuariosInscritos"] = inscritos
        db['evento'].save(evento)
    else:

        inscritos = list(inscritos)
        if usuario in inscritos:
            if (momentoFimInscricao == None) or (momentoFimInscricao >= datetime.now()):
                inscritos.remove(usuario)
                evento["usuariosInscritos"] = inscritos
                evento["inscricoes"] = evento["inscricoes"] - 1
                db['evento'].save(evento)
            else:
                return 'fimDasInscriçoes', 876

        else:
            if (momentoFimInscricao == None) or (momentoFimInscricao >= datetime.now()):
                inscritos.append(usuario)
                evento["usuariosInscritos"] = inscritos
                evento["inscricoes"] = evento["inscricoes"]+1
                db['evento'].save(evento)
            else:
                return 'fimDasInscriçoes', 876

    return 'ok', 200

@app.route("/cadastrarEvento", methods=["POST", "GET"])
@login_required
def cadastrarEvento():
    if request.method == 'GET':
        return render_template("eventoCadastro.html")

    if request.method == 'POST':
        evento = Evento()

        evento.titulo = request.form.get("tTitulo",'')
        evento.categoria = request.form.get("selCategoria",'')
        evento.descricao = request.form.get("tDescricao",'')
        evento.imagem = request.form.get("fileBase64",'')
        evento.momentoExecucao = request.form.get("tDataEvento", None)
        evento.local = request.form.get("tLocal",'')
        evento.pontos = int(request.form.get("tPontos",0))
        evento.vagas = int(request.form.get("tVagas",0))
        evento.inscricoes = 0
        evento.usuariosInscritos = []
        evento.publicado = "N"
        evento.momentoFimInscricao = request.form.get("tDataFimInscricao", None)
        evento.momentoCadastro = datetime.now()
        evento.concluido = "N"

        if not evento.momentoExecucao == None:
            evento.momentoExecucao = datetime.strptime(evento.momentoExecucao,"%Y/%m/%d %H:%M")

        if not evento.momentoFimInscricao == None:
            evento.momentoFimInscricao = datetime.strptime(evento.momentoFimInscricao, "%Y/%m/%d %H:%M")

        # Salvando no banco
        db = utilitariosDB.getDb()
        evento.salvarMongoDb(db)

        return 'ok', 200

@app.route("/postConcluir", methods=["POST"])
@login_required
def postConcluir():

    cont = json.loads(request.data.decode('utf-8'))
    eventoId = cont.get('eventoId','')

    db = utilitariosDB.getDb()
    evento = db['evento'].find_one({"_id":ObjectId(eventoId)})
    concluido = evento.get('concluido', None)

    if (concluido == None) or (concluido == "N"):
        evento["concluido"] = "S"
        db['evento'].save(evento)
    else:
        evento["concluido"] = "N"
        db['evento'].save(evento)

    return 'ok', 200


@app.route("/postPublicar", methods=["POST"])
@login_required
def postPublicar():

    cont = json.loads(request.data.decode('utf-8'))
    eventoId = cont.get('eventoId','')

    db = utilitariosDB.getDb()
    evento = db['evento'].find_one({"_id":ObjectId(eventoId)})
    publicado = evento.get('publicado', None)

    if (publicado == None) or (publicado == "N"):
        evento["publicado"] = "S"
        db['evento'].save(evento)
    else:
        evento["publicado"] = "N"
        db['evento'].save(evento)

    return 'ok', 200


if __name__ == "__main__":
    app.run(threaded=True, debug=True, host="0.0.0.0", port="5000")
