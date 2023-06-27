from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from Usuarios.models import Avatar


admin.site.register(User, UserAdmin, Avatar)
