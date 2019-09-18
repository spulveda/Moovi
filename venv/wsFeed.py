import appPadrao
from flask_login import UserMixin
from classes import Usuario
from flask import *
from flask_login import LoginManager, login_required, login_user, logout_user
import utilitariosDB

app = appPadrao.criar_appPadrao()

@app.route('/feed', methods=['GET'])
@login_required
def feed():

    db = utilitariosDB.getDb()
    posts = db['post'].find().limit(10)
    post = ''
    for i in posts:
        titulo = i['titulo']
        midia = i['midia']
        midiaTipo = i['midiaTipo']
        descricao = i['descricao']

        pt = ('<div class="card shadow mb-4">'
                    '<div class="card-header py-3">'
                      '<h6 class="m-0 font-weight-bold text-primary">'+titulo+'</h6>'
                    '</div>'
                    '<div class="card-body">')

        if (midiaTipo == "imgB64"):
            pt = pt+('<div class="text-center">'
                        '<img class="img-fluid px-3 px-sm-4 mt-3 mb-4" style="width: 25rem;" src="'+midia+'" alt="">'
                      '</div>')

        pt = pt+('<p>'+descricao+'</p>'                      
                    '</div>'
                  '</div>' )

        post = post+pt

    return render_template('feed.html',postMsg=Markup(post))

if __name__ == "__main__":
    app.run(threaded=True ,debug=True,host="0.0.0.0",port="5000")
