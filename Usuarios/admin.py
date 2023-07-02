from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Avatar, Perfil
from django.utils.html import format_html
from PIL import Image


class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = True


class AvatarInline(admin.StackedInline):
    model = Avatar
    can_delete = True


# Desregistrar UserAdmin del administrador principal
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    inlines = (PerfilInline, AvatarInline)

    def delete_model(self, request, obj):
        perfil = obj.perfil
        avatar = obj.avatar
        if perfil:
            perfil.delete()
            # Crear una instancia vacía de Perfil asociada al usuario
            try:
                Perfil.objects.create(user=obj)
            except:
                pass
        if avatar:
            avatar.delete()
            # Crear una instancia vacía de Avatar asociada al usuario
            try:
                Avatar.objects.create(user=obj)
            except:
                pass
        super().delete_model(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            # Verificar si el usuario es superusuario
            if request.user.is_superuser:
                return True
            # No permitir la eliminación directa de perfiles y avatares
            return False
        return False


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ['id', 'preview_image', 'get_user_name']
    readonly_fields = ['preview_image']

    def preview_image(self, obj):
        if obj.image:
            img = Image.open(obj.image)
            img.thumbnail((300, 300))
            return format_html('<img src="{}" width="{}" height="{}" />', obj.image.url, img.width, img.height)
        else:
            return '(No image)'

    preview_image.short_description = 'Preview'

    def get_user_name(self, obj):
        return obj.user.username

    get_user_name.short_description = 'User'

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        # Crear una instancia vacía de Avatar asociada al usuario
        Avatar.objects.create(user=obj.user)

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            # Verificar si el usuario es superusuario
            if request.user.is_superuser:
                return True
            # No permitir la eliminación directa de avatares
            return False
        return False


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)
    fields = ('user', 'fecha_nacimiento', 'pais_nacimiento', 'residencia', 'institucion', 'cargo')
    list_display = ('get_user_name', 'fecha_nacimiento', 'pais_nacimiento')

    def get_user_name(self, obj):
        return obj.user.username

    get_user_name.short_description = 'User'

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        # Crear una instancia vacía de Perfil asociada al usuario
        Perfil.objects.create(user=obj.user)

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            # Verificar si el usuario es superusuario
            if request.user.is_superuser:
                return True
            # No permitir la eliminación directa de perfiles
            return False
        return False
