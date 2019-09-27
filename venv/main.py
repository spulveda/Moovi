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

app = appPadrao.criar_appPadrao()

@app.route("/", methods=["GET"])
@login_required
def index():
    return render_template("index.html")

# ----------    Inicio da Evento  --------------#
@app.route('/getEvento', methods=['GET'])
@login_required
def getEventoEp():
    return wsEvento.getEvento()

@app.route('/postInscreverse',methods=["POST"])
@login_required
def postInscreverse():
    return wsEvento.postInscreverse()

@app.route("/cadastrarEvento", methods=["POST", "GET"])
@login_required
def cadastrarEvento():
    return wsEvento.cadastrarEvento()

@app.route("/postConcluir", methods=["POST"])
@login_required
def postConcluir():
    return wsEvento.postConcluir()

@app.route("/postPublicar", methods=["POST"])
@login_required
def postPublicar():
    return wsEvento.postPublicar()

# ----------    Inicio da agenda  --------------#
@app.route('/getAgenda', methods=['GET'])
@login_required
def getAgenda():
    return agenda.getAgenda()

# ----------    Inicio da agenda  --------------#
@app.route('/feedLoad', methods=['GET'])
@login_required
def feedLoad():
    return wsFeed.feedLoad()

@app.route('/feedInsert', methods=['GET', 'POST'])
@login_required
def feedInsert():
    return wsFeed.feedInsert()

@app.route('/getComentarios', methods=['GET'])
@login_required
def getComentario():
    return wsFeed.getComentario()

@app.route('/postComentarios', methods=['POST'])
@login_required
def postComentario():
    return wsFeed.postComentario()

if __name__ == "__main__":
    app.run(threaded=True, debug=True, host="0.0.0.0", port="5000")
