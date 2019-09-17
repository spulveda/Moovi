# -*- coding: utf-8 -*-

import classes
import utilitariosDB

a = classes.Usuario()
a.nome = "nome teste3"
a.email = "emailtesasdasdasdasdte@email.com.br"
a.senha = "123"

#db = utilitariosDB.getDb(db="testes")

#a.salvarMongoDb(db)

print(utilitariosDB.loginUsuario(a))

#b = classes.Usuario()
#b.fromJson({"nome":"tete2"})
#print(b.nome)

