import appPadrao
from flask_login import UserMixin
from classes import Usuario
from flask import *
from flask_login import LoginManager, login_required, login_user, logout_user

app = appPadrao.criar_appPadrao()

@app.route('/feed', methods=['GET'])
#habilitar assim que estiver em produção
@login_required
def feed():
    return render_template('feed.html')

if __name__ == "__main__":
    app.run(threaded=True ,debug=True,host="0.0.0.0",port="5000")
