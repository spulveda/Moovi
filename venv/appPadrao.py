# -*- coding: utf-8 -*-
from flask_login import UserMixin, current_user
from classes import Usuario
from flask import *
from flask_login import LoginManager, login_required, login_user, logout_user
import appConfigPython
import os
import utilitariosDB
from bson.objectid import ObjectId

def criar_appPadrao():

    app = Flask(__name__, instance_relative_config=False)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'

    # config
    app.config.from_object("appConfigPython.Config")
    # flask-login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.session_protection = "strong"

    # logica de login
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == 'POST':

            username = request.form['inputEmail']
            password = request.form['inputPassword']

            usuario = Usuario()
            usuario.fromJson({"email": username, "senha": password})
            user = utilitariosDB.loginUsuario(usuario)
            if not (usuario is None):
                user = Usuario(user)
                login_user(user, remember=True)
                return redirect(request.args.get("next"))
            else:
                return abort(401)
        else:
            return render_template('Login.html')

    # logout
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    # se der erro no login podemos fazer assim
    @app.errorhandler(401)
    def page_not_found(e):
        return Response('<p>Login failed</p>')

    # callback to reload the user object
    @login_manager.user_loader
    def load_user(_id):
        user = Usuario()
        user._id = _id
        return user

    @app.route("/getNavBar", methods=["GET"])
    @login_required
    def getNavBar():

        usuarioAtivo = current_user.get_id()
        db = utilitariosDB.getDb()
        usuario = db['usuarios'].find_one({"_id": ObjectId(usuarioAtivo)})

        usuario.get('imagem',"")

        nav = ""

        nav = ('<nav class="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow">'
                  '<a class="navbar-brand" href="/feed">MOOVI <sup>CNS</sup></a>'                    
                  '<ul class="navbar-nav ml-auto">'                        
                    '<div class="topbar-divider d-none d-sm-block"></div>'
                    
                    '<li class="nav-item dropdown no-arrow">'
                      '<a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
                        '<span class="mr-2 d-lg-inline text-gray-600 small">'+usuario.get('nome',"")+'</span>'
                        '<img class="img-profile rounded-circle" src="'+usuario.get('imagem',"")+'">'
                      '</a>'
                      
                      '<div class="dropdown-menu dropdown-menu-right shadow animated--grow-in" aria-labelledby="userDropdown">'                
                        '<a class="dropdown-item" href="#" data-toggle="modal" data-target="#logoutModal">'
                          '<i class="fas fa-sign-out-alt fa-sm fa-fw mr-0 text-gray-400"></i>'
                          'Logout'
                        '</a>'
                      '</div>'
                    '</li>'
                  '</ul>'
                '</nav>')


        return Markup(nav)


    return app

