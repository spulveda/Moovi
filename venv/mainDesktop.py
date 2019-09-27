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

app = appPadrao.criar_appPadrao()

@app.route("/", methods=["GET"])
@login_required
def index():
    return render_template("indexDesktop.html")

@app.route("/getUsuarios", methods=["GET"])
@login_required
def getLoadUsuarios():
    return wsUsuario.getLoadUsuarios()

if __name__ == "__main__":
    app.run(threaded=True, debug=True, host="0.0.0.0", port="5000")
