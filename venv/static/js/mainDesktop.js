    <!-- Cadastro de usuário -->    
    var ultimoUsuarioClicado
    
    function updateCards(cards){        
        document.getElementById("divContainerPrincipal").innerHTML = cards;
          
      };
    function liberarUsuario(){
      
        var xmlHttp = new XMLHttpRequest();            
        xmlHttp.onreadystatechange = function() { 
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
                $('#'+ultimoUsuarioClicado).html(xmlHttp.responseText)
        }
        xmlHttp.open("GET", "/liberarBloquearUsuario?usuarioid="+ultimoUsuarioClicado, true); // true for asynchronous 
        xmlHttp.send();            

        $('#modalEditorUsuario').modal('toggle')
    };

    function editarUsuario(ele){        
        ultimoUsuarioClicado = ele.id
        $('#modalEditorUsuario').modal('show')
    };

<!-- Adm Atividades -->
    
        function publicarEvento(ele){
            var xmlHttp = new XMLHttpRequest();
            var eventoId = ele.parentElement.parentElement.id;                        
            xmlHttp.onreadystatechange = function() {
                if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
                    location.reload();
                }
            }
            xmlHttp.open("POST", "/postPublicar", true);                        
            xmlHttp.send(JSON.stringify({"eventoId":eventoId}));
            
        }
        
        function concluirEvento(ele){
            var xmlHttp = new XMLHttpRequest();
            var eventoId = ele.parentElement.parentElement.id;                        
            xmlHttp.onreadystatechange = function() {
                if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
                    location.reload();
                }
            }
            xmlHttp.open("POST", "/postConcluir", true);                        
            xmlHttp.send(JSON.stringify({"eventoId":eventoId}));
            
        }


