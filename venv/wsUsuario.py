import classes

a = classes.Usuario()
a.usuarioId = "asd"
a.nome = "nome teste"
a.email = "emailteste@email.com.br"


print(a.getJson())