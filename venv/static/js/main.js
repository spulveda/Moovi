 <!-- Inicio principal -->
function onloadScroll(local){
        getNavBar();
        getOnLoadEventos();          
      };

        function updateNavBar(nav){        
            document.getElementById("content").insertAdjacentHTML("afterbegin",nav);
          
        };      
        
        function getNavBar() {
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.onreadystatechange = function() { 
                if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
                    updateNavBar(xmlHttp.responseText);                
            }
            xmlHttp.open("GET", "/getNavBar", true); // true for asynchronous 
            xmlHttp.send();            
        };
        
      function updateCards(cards){        
        document.getElementById("divContainerPrincipal").innerHTML = cards;
          
      };

 <!-- Inicio evento -->
      function getOnLoadEventos() {
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.onreadystatechange = function() { 
                if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
                    updateCards(xmlHttp.responseText);                
            }
            xmlHttp.open("GET", "/getEvento", true); // true for asynchronous 
            xmlHttp.send();            
      };
    
        function postInscreverse(ele){
            var xmlHttp = new XMLHttpRequest();
            var eventoId = ele.id;                        
            xmlHttp.onreadystatechange = function() {
                if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
                    getOnLoadEventos();
                }else{
                 if (xmlHttp.readyState == 4 && xmlHttp.status == 876)
                    alert("Inscrições finalizadas.");   
                }                                    
            }
            xmlHttp.open("POST", "/postInscreverse", true);                        
            xmlHttp.send(JSON.stringify({"eventoId":eventoId}));
        };   

        function publicar(ele){
            var xmlHttp = new XMLHttpRequest();
            var eventoId = ele.id;                        
            xmlHttp.onreadystatechange = function() {
                if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
                    getOnLoadEventos();
                }
            }
            xmlHttp.open("POST", "/postPublicar", true);                        
            xmlHttp.send(JSON.stringify({"eventoId":eventoId}));
            
        }
        
        function concluir(ele){
            var xmlHttp = new XMLHttpRequest();
            var eventoId = ele.id;                        
            xmlHttp.onreadystatechange = function() {
                if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
                    getOnLoadEventos();
                }
            }
            xmlHttp.open("POST", "/postConcluir", true);                        
            xmlHttp.send(JSON.stringify({"eventoId":eventoId}));
            
        }

 <!-- Inicio agenda -->
      function getOnLoadAgenda() {
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.onreadystatechange = function() { 
                if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
                    updateCards(xmlHttp.responseText);                
            }
            xmlHttp.open("GET", "/getAgenda", true); // true for asynchronous 
            xmlHttp.send();            
      };

<!-- Inicio feed -->
var itens = 0

        function getOnLoadFeed() {
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.onreadystatechange = function() { 
                if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
                    updateCards(xmlHttp.responseText);
            }
            xmlHttp.open("GET", "/feedLoad?item="+itens, true); // true for asynchronous 
            xmlHttp.send();
            itens += 1;
        };

        function loadComentario(comentId,cards,limpar){
            if (limpar == true) {
                var ele = document.getElementById("postFooter"+comentId)
                var post = ele.parentElement.parentElement
                var postDiv = ele.parentElement.parentElement
                if (postDiv.className == "border-left-primary"){
                    postDiv.innerHTML = ""; 
                    post.innerHTML = cards;  
                }else{
                    ele.innerHTML = cards;  
                }
                                              
            }else{
                var ele = document.getElementById("postFooter"+comentId)
                ele.innerHTML = cards;                            
            }
            
        };
      
        function getloadComentario(ele,idPost) {
            var xmlHttp = new XMLHttpRequest();
            var postId = idPost;
            var limpar = true
            if (typeof postId == "undefined") {
                var postId = ele.id;    
                limpar = false
            }            
            xmlHttp.onreadystatechange = function() { 
                if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
                    loadComentario(postId,xmlHttp.responseText,limpar);
            }
            xmlHttp.open("GET", "/getComentarios?postId="+postId, true); // true for asynchronous 
            xmlHttp.send();
            itens += 1;
        };
                  
        var postCallBackElement
        function postComentario(ele){
            var xmlHttp = new XMLHttpRequest();
            var postId = ele.parentElement.id;
            var comentario = ele.previousSibling.value;
            postCallBackElement = ele
            xmlHttp.onreadystatechange = function() {
                if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
                    getloadComentario(postCallBackElement,postId);
            }
            xmlHttp.open("POST", "/postComentarios", true);                        
            xmlHttp.send(JSON.stringify({"post":postId, "comentario":comentario}));
        };
      
        window.onscroll = function(ev) {
            if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
                getOnLoadFeed();
            }
        };