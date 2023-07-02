from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver

class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Usuarios'

    def ready(self):
        import Usuarios.signals  # Importa las señales aquí
