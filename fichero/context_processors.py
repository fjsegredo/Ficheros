# archivo para pasar contexto automáticamente a todas las páginas
from django.urls import resolve
from django.contrib.auth.models import User
from Usuarios.models import Avatar, Perfil
from django.core.exceptions import ObjectDoesNotExist

def user_context(request):
    return {
        'user': request.user
    }

def user_avatar(request):
    user = request.user
    avatar = None
    avatar_exists = False

    if user.is_authenticated:
        try:
            avatar = Avatar.objects.get(user=user)
            avatar_exists = True
        except Avatar.DoesNotExist:
            pass

    return {'user': user, 'avatar': avatar, 'avatar_exists': avatar_exists}

def user_perfil(request):
    user = request.user
    perfil = None

    if user.is_authenticated:
        try:
            perfil = Perfil.objects.get(user=user)
        except Perfil.DoesNotExist:
            pass

    return {'user': user, 'perfil': perfil}