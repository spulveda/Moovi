var activePage

    function updateCards(cards){        
        document.getElementById("divContainerPrincipal").innerHTML = cards;
          
      };

    <!-- Inicio agenda -->
      function getOnLoadUsuarios() {
            var xmlHttp = new XMLHttpRequest();
            activePage = "USUARIOS"
            xmlHttp.onreadystatechange = function() { 
                if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
                    updateCards(xmlHttp.responseText);                
            }
            xmlHttp.open("GET", "/getUsuarios", true); // true for asynchronous 
            xmlHttp.send();            
      };
