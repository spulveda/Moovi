# -*- coding: utf-8 -*-

import classes
import utilitariosDB

a = classes.Usuario()
a.nome = "nome teste"
a.email = "a"
a.senha = "a"

db = utilitariosDB.getDb(db="testes")

a.salvarMongoDb(db)

print(utilitariosDB.loginUsuario(a))

#b = classes.Usuario()
#b.fromJson({"nome":"tete2"})
#print(b.nome)

