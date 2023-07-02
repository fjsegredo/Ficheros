from django.apps import AppConfig

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myproject'

    def ready(self):
        # Importa las señales de las aplicaciones secundarias
        import Usuarios.signals
        # import otras_aplicaciones.signals
        # import ...

# Actualiza el valor de 'MyAppConfig' con el nombre de tu configuración de la aplicación raíz
default_app_config = 'myproject.apps.MyAppConfig'
