import base64

def arquivoParaBase64(arquivo):
    with open(arquivo, "rb") as file:
        return base64.b64encode(file.read())



#cores para os templates

# compartilha #e47423
# participa  #ff0101

#-- Side bar dos layaouts para desktop
def getSideBar():
    sideBar = ('<!-- Sidebar -->'
               '<ul class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">'

               '<!-- Sidebar - Brand -->'
               '<a class="sidebar-brand d-flex align-items-center justify-content-center" href="index.html">'
               '<div class="sidebar-brand-icon rotate-n-15">'
               '<i class="fas fa-laugh-wink"></i>'
               '</div>'
               '<div class="sidebar-brand-text mx-3">Moovi <sup>ADM</sup></div>'
               '</a>'

               '<!-- Divider -->'
               '<hr class="sidebar-divider my-0">'

               '<!-- Nav Item - adm feedback -->'
               '<li class="nav-item active">'
               '<a class="nav-link" href="/admfeedback">'
               '<i class="fas fa-fw fa-tachometer-alt"></i>'
               '<span>FeedBacks</span></a>'

               '</li>'

               '<!-- Divider -->'
               '<hr class="sidebar-divider">'

               '<!-- Heading -->'
               '<div class="sidebar-heading">'

               '</div>'

               '<!-- Nav Item - Pages Collapse Menu -->'
               '<li class="nav-item">'
               '<a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="true" aria-controls="collapseTwo">'
               '<i class="fas fa-fw fa-cog"></i>'
               '<span>Cadastro</span>'
               '</a>'
               '<div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#accordionSidebar">'
               '<div class="bg-white py-2 collapse-inner rounded">'
               '<a class="collapse-item" href="/admusuarios">Usuários</a>'
               '<a class="collapse-item" href="/admatividades">Atividades</a>'
               '<a class="collapse-item" href="/admfeed">Feed</a>'
               '</div>'
               '</div>'
               '</li>'

               '<!-- Divider -->'
               '<hr class="sidebar-divider d-none d-md-block">'

               '<!-- Sidebar Toggler (Sidebar) -->'
               '<div class="text-center d-none d-md-inline">'
               '<button class="rounded-circle border-0" id="sidebarToggle"></button>'
               '</div>'

               '</ul>'
               '<!-- End of Sidebar -->')

    return sideBar


def getNavBar(usuario):
    usuario.get('imagem', "")

    nav = ""

    nav = ('<nav class="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow">'
           '<a class="navbar-brand" href="/feed">MOOVI <sup>CNS</sup></a>'
           '<ul class="navbar-nav ml-auto">'
           '<div class="topbar-divider d-none d-sm-block"></div>'

           '<li class="nav-item dropdown no-arrow">'
           '<a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
           '<span class="mr-2 d-lg-inline text-gray-600 small">' + usuario.get('nome', "") + '</span>'
                                                                                             '<img class="img-profile rounded-circle" src="' + usuario.get(
        'imagem', "") + '">'
                        '</a>'

                        '<div class="dropdown-menu dropdown-menu-right shadow animated--grow-in" aria-labelledby="userDropdown">'
                        '<a class="dropdown-item" href="#" data-toggle="modal" data-target="#logoutModal">'
                        '<i class="fas fa-sign-out-alt fa-sm fa-fw mr-0 text-gray-400"></i>'
                        'Logout'
                        '</a>'
                        '</div>'
                        '</li>'
                        '</ul>'
                        '</nav>')

    return nav
