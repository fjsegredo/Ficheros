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
from .views import inicio, about
from Usuarios.views import RegistroVista, LoginVista, LogoutVista, EditarPerfil, contribuyentes, ver_perfil

urlpatterns = [
    path('', inicio, name='inicio'),
    path('registro/', RegistroVista.as_view(), name='registro'),
    path('admin/', admin.site.urls),
    path("about/", about, name='about'),
    path('accounts/login/', LoginVista.as_view(), name='login'),
    path('logout/', LogoutVista, name='logout'),
    path('perfil/', EditarPerfil, name='perfil'),
    path('contribuyentes/', contribuyentes, name='contribuyentes'),
    path('perfil/<str:username>/', ver_perfil, name='ver_perfil')
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

