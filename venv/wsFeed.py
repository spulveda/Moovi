import appPadrao
from flask_login import UserMixin, current_user
from classes import Usuario,Post, Comentarios
from flask import *
from flask_login import LoginManager, login_required, login_user, logout_user
import utilitariosDB
from datetime import datetime
import pymongo
from bson.objectid import ObjectId

app = appPadrao.criar_appPadrao()

@app.route('/feedLoad', methods=['GET'])
@login_required
def feedLoad():
    nItens = request.args.get('item',0)

    if nItens == 0:
        db = utilitariosDB.getDb()
        posts = db['post'].find().limit(10).sort([("momento", pymongo.DESCENDING)])

    else:
        db = utilitariosDB.getDb()
        posts = db['post'].find().limit(int(nItens)*10).sort([("momento", pymongo.DESCENDING)])

    post = ''
    for i in posts:
        titulo = i.get('titulo', '')
        midia = i.get('midia','')
        midiaTipo = i.get('midiaTipo','')
        descricao = i.get('descricao','')
        postId = i.get('_id','')

        descricao = "<br />".join(descricao.split("\n"))

        pt = ('<div class="card shadow mb-4">'
                    '<div class="card-header py-3">'
                      '<h6 class="m-0 font-weight-bold text-primary text-center">'+titulo+'</h6>'
                    '</div>'
                    '<div class="card-body">')

        if (midiaTipo == "imgB64") and (midia != ""):
            pt = pt+('<div class="text-center">'
                        '<img class="img-fluid px-3 px-sm-4 mt-3 mb-4" style="width: 25rem;" src="'+midia+'" alt="">'
                      '</div>')

        pt = pt+('<p>'+descricao+'</p>'                      
                    '</div>'
                   '<div  >'
                  '<i id="'+str(postId)+'" class="fas fa-comments fa-2x text-gray-300 float-right mb-2 col-md-auto" onclick="getloadComentario(this)" style="color: f6c23e!important" ></i>'
                '</div>'    
                                        
                    '<div class="card-footer" id="postFooter'+str(postId)+'">'
                      '<small class="text-muted">Comentarios...</small>'
                    '</div>'

                  '</div>' )

        post = post+pt

    return Markup(post)

@app.route('/feed', methods=['GET'])
@login_required
def feed():
      return render_template('feed.html')

@app.route('/feedInsert', methods=['GET', 'POST'])
@login_required
def feedInsert():
    if request.method == 'POST':

        post = Post()
        post.titulo = request.form.get("feedInTitulo",'')
        post.descricao = request.form.get("feedInMensagem",'')
        post.midiaTipo = "imgB64"
        post.midia = request.form.get("fileBase64",'')
        post.momento = datetime.now()

        # Salvando no banco
        db = utilitariosDB.getDb()
        post.salvarMongoDb(db)

        return redirect("/feed")
    else:
        return render_template("feedInsert.html")


@app.route('/getComentarios', methods=['GET'])
@login_required
def getComentario():
    if request.method == 'GET':
        post = request.args.get('postId')
        cm = ""
        if (post > ''):
            db = utilitariosDB.getDb()
            comentarios = db['comentarios'].find({"post":post})
            for coment in comentarios:

                usuario = db['usuarios'].find_one({"_id":ObjectId(coment.get("usuario"))})
                if (usuario == None):
                    return None

                imagem = usuario.get("imagem",'')
                nome = usuario.get("nome",'')
                texto = coment.get("comentario",'')

                cm += ('<div class="border-left-primary">' 
                        '<a class="dropdown-item d-flex align-items-center s">'
                          '<div class="mr-6 ">')

                if (imagem > ''):
                    cm += '<img class="img-profile rounded-circle img-fluid px-3 px-sm-4 mt-1 mb-4" style="width: 5rem;" src="' + imagem + '" alt="">'

                cm += (   '</div>'
                          '<div id="'+post+'">'
                            '<div class="small text-gray-500 mt-0 mb-0"><h6 style="width: 8rem;">'
                                +nome+'</h6>'
                                '<p class="font-italic mt-0">'+texto+'</p>'     
                            '</div>'                                
                          '</div>'
                         '</a> '
                        '</div>')


            if cm == '':
                cm = ('<div id="' + post + '" class="input-group">'                       
                        '<input type="text" class="form-control mr-1" name="feedComentario" id="feedComentario'+post+'" placeholder="Comentar..."  >'
                        '<button  class="btn btn-info btn-circle mr-0" onclick="postComentario(this)">'
                            '<i class="fas fa-check"></i>'
                        '</button>'
                        
                    '</div>')
            else:
                cm += ('<div id="' + post + '" class="input-group">'
                                           '<input type="text" class="form-control mr-1 " name="feedComentario" id="feedComentario' + post + '" placeholder="Comentar..."  >'
                                            '<button  class="btn btn-info btn-circle  mr-0" onclick="postComentario(this)">'
                                                '<i class="fas fa-check"></i>'
                                            '</button>'
                                            '</div>')


        return Markup(cm)


@app.route('/postComentarios', methods=['POST'])
@login_required
def postComentario():
    cont = json.loads(request.data.decode('utf-8'))
    post = cont.get('post','')
    coment = cont.get('comentario','')

    if (coment >""):
        comentario = Comentarios()
        comentario.post = post
        comentario.comentario = coment
        comentario.momento = datetime.now()
        comentario.usuario = current_user.get_id()

        # Salvando no banco
        db = utilitariosDB.getDb()
        comentario.salvarMongoDb(db)

    return '', 200



if __name__ == "__main__":
    app.run(threaded=True ,debug=True,host="0.0.0.0",port="5000")
