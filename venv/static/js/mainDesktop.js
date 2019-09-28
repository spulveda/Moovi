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


