import classes
import utilitariosDB

a = classes.Usuario()
a.usuarioId = "asd"
a.nome = "nome teste"
a.email = "emailteste@email.com.br"

db = utilitariosDB.getDb(db="testes")

a.salvarMongoDb(db)