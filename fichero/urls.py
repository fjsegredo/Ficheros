"""
URL configuration for fichero project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.utils.translation import gettext as _
from django.contrib import admin
from django.urls import path
from .views import inicio, about, fichar
from Usuarios.views import cambiar_pass, RegistroVista, LoginVista, LogoutVista, EditarPerfil, contribuyentes, ver_perfil
from Fichas.views import CrearFicha, buscar_libros, buscar_fichas, fichas_por_libro, agregar_libro, libros, ver_libro, articulos, ver_articulo, agregar_articulo, agregar_capitulo, capitulos, ver_capitulo

urlpatterns = [
    path('', inicio, name='inicio'),
    path('registro/', RegistroVista.as_view(), name='registro'),
    path('perfil/cambiar_pass', cambiar_pass, name='cambiar_pass'),
    path('admin/', admin.site.urls),
    path("about/", about, name='about'),
    path('accounts/login/', LoginVista.as_view(), name='login'),
    path('logout/', LogoutVista, name='logout'),
    path('perfil/', EditarPerfil, name='perfil'),
    path('contribuyentes/', contribuyentes, name='contribuyentes'),
    path('perfil/<str:username>/', ver_perfil, name='ver_perfil'),
    path('fichar', fichar, name='fichar'),
    path('libros/<int:id>/crear_ficha', CrearFicha, name='crear_ficha'),
    path('fichar/agregar_libro', agregar_libro, name='agregar_libro'),
    path('fichar/agregar_articulo', agregar_articulo, name='agregar_articulo'),
    path('fichar/agregar_capitulo', agregar_capitulo, name='agregar_capitulo'),
    path('libros', libros, name='libros'),
    path('libros/<int:id>', ver_libro, name='ver_libro'),
    path('libros/articulos', articulos, name='articulos'),
    path('libros/articulos/<int:id>', ver_articulo, name='ver_articulo'),
    path('libros/capitulos', capitulos, name='capitulos'),
    path('libros/capitulos/<int:id>', ver_capitulo, name='ver_capitulo'),
    path('libros/<int:libro_id>/fichas', fichas_por_libro, name='fichas_por_libro'),
    path('buscar/libros', buscar_libros, name='buscar_libros'),
    path('buscar/fichas', buscar_fichas, name='buscar_fichas'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

