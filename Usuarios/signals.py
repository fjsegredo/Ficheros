from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from Usuarios.models import Avatar, Perfil

@receiver(post_delete, sender=User)
def delete_user_related_objects(sender, instance, **kwargs):
    try:
        avatar = instance.avatar
        if avatar:
            avatar.delete()
    except Avatar.DoesNotExist:
        pass

    try:
        perfil = instance.perfil
        if perfil:
            perfil.delete()
    except Perfil.DoesNotExist:
        pass


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Crea un avatar vacío asociado al nuevo usuario
        Avatar.objects.create(user=instance)

        # Crea un perfil vacío asociado al nuevo usuario
        Perfil.objects.create(user=instance)
