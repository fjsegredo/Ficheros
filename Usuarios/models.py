from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os
from PIL import Image

def avatar_path(instance, filename):
    username = instance.user.username
    extension = os.path.splitext(filename)[1]
    unique_filename = f"{username}{extension}"
    return os.path.join('avatars', unique_filename)

class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=avatar_path, null=True)
    
    def __str__(self):
        return self.user.username
    
    @property
    def mostrar(self):
        if self.image:
            return self.image.url
        else:
            default_avatar_path = os.path.join(settings.MEDIA_ROOT, 'defaultavatar.jpg')
            if os.path.exists(default_avatar_path):
                return os.path.join(settings.MEDIA_URL, 'defaultavatar.jpg')
            else:
                return ''

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField(null=True)
    pais_nacimiento = models.CharField(max_length=100, null=True)
    residencia = models.CharField(max_length=100, null=True)
    institucion = models.CharField(max_length=100, null=True)
    cargo = models.CharField(max_length=100, null=True)
    pagina_web = models.URLField(null=True)

    class Meta:
        verbose_name_plural = "Perfiles"
        
    def __str__(self):
        return (self.user.username)
    
    def extendido(self):
        atributos = vars(self)
        perfil_extendido = [(key, value) for key, value in atributos.items() if not key.startswith('_')]
        return perfil_extendido
    
    
