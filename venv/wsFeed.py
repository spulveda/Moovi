import appPadrao
from flask_login import UserMixin
from classes import Usuario,Post
from flask import *
from flask_login import LoginManager, login_required, login_user, logout_user
import utilitariosDB
from datetime import datetime

app = appPadrao.criar_appPadrao()

@app.route('/feed', methods=['GET'])
@login_required
def feed():

    db = utilitariosDB.getDb()
    posts = db['post'].find().limit(10)
    post = ''
    for i in posts:

        titulo = i.get('titulo', '')
        midia = i.get('midia','')
        midiaTipo = i.get('midiaTipo','')
        descricao = i.get('descricao','')

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

@app.route('/feedInsert', methods=['GET', 'POST'])
def feedInsert():
    if request.method == 'POST':

        post = Post()
        post.titulo = request.form.get("feedInTitulo",'')
        post.descricao = request.form.get("feedInMensagem",)
        post.midiaTipo = "imgB64"
        post.midia = request.form.get("fileBase64",)
        post.momento = datetime.now()

        # Salvando no banco
        db = utilitariosDB.getDb()
        post.salvarMongoDb(db)

        return redirect("feed.html")
    else:
        return render_template("feedInsert.html")

if __name__ == "__main__":
    app.run(threaded=True ,debug=True,host="0.0.0.0",port="5000")
