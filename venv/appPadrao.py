# -*- coding: utf-8 -*-
from flask_login import UserMixin
from classes import Usuario
from flask import *
from flask_login import LoginManager, login_required, login_user, logout_user
import appConfigPython
import os
import utilitariosDB


def criar_appPadrao():

    app = Flask(__name__, instance_relative_config=False)

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
        try:

            if request.method == 'POST':

                username = request.form['inputEmail']
                password = request.form['inputPassword']

                usuario = Usuario()
                usuario.fromJson({"nome": username, "senha": password})
                user = utilitariosDB.loginUsuario(usuario)

                if not (user is None):
                    login_user(user, remember=True)
                    return redirect(request.args.get("next"))
                else:
                    return abort(401)
            else:
                return render_template('Login.html')
        except:
            return render_template("login.html")

    # logout
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return Response('<p>Logged out</p>')

    # se der erro no login podemos fazer assim
    @app.errorhandler(401)
    def page_not_found(e):
        return Response('<p>Login failed</p>')

    # callback to reload the user object
    @login_manager.user_loader
    def load_user(userid):
        return User(userid)


    return app

