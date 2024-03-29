import appPadrao
from flask_login import UserMixin, current_user
from classes import Usuario, Evento
from flask import *
from flask_login import LoginManager, login_required, login_user, logout_user
import utilitariosDB
from datetime import datetime
import pymongo
from bson.objectid import ObjectId
import agenda
import wsEvento
import wsFeed
import wsUsuario
import wsAtividades
from utils import getSideBar, getNavBar

app = appPadrao.criar_appPadrao()

@app.route("/", methods=["GET"])
@login_required
def index():
    sideBar = Markup(getSideBar())

    usuarioAtivo = current_user.get_id()
    db = utilitariosDB.getDb()
    usuario = db['usuarios'].find_one({"_id": ObjectId(usuarioAtivo)})
    navbar = Markup(getNavBar(usuario))

    return render_template("indexDesktop.html", sideBarWS=sideBar, navbarWS=navbar)

#--   USUARIOS ---
@app.route("/admusuarios", methods=["GET"])
@login_required
def getLoadUsuarios():
    return wsUsuario.getLoadUsuarios()

@app.route("/liberarBloquearUsuario", methods=["GET"])
@login_required
def postLiberarBloquearUsuario():
    usuarioid = request.args.get('usuarioid', None)
    if usuarioid != None:
        return wsUsuario.liberarUsuario(usuarioid)

#--  DASH --
@app.route("/dashDesktop", methods=["GET"])
@login_required
def getDashDesktop():
    return "Ainda não implementado"

#-- ATIVIDADES --
@app.route("/admfeedback", methods=["GET"])
@login_required
def getAdmFeedBack():
    return wsAtividades.getAdmFeedBack();

@app.route("/admatividades", methods=["GET"])
@login_required
def getLoadAtividades():
    return wsAtividades.getLoadAtividades();

@app.route("/postPublicar", methods=["POST"])
@login_required
def postPublicar():
    wsEvento.postPublicar()
    return 'ok', 200

@app.route("/postConcluir", methods=["POST"])
@login_required
def postConcluir():
    wsEvento.postConcluir()
    return 'ok', 200

@app.route("/cadadmatividades", methods=["GET", "POST"])
@login_required
def cadAdmAtividades():
    return wsAtividades.cadAdmAtividades()

@app.route("/admfeed", methods=["GET","POST"])
@login_required
def admFeed():
    return wsFeed.admFeed()


if __name__ == "__main__":
    app.run(threaded=True, debug=True, host="0.0.0.0", port="5000")
