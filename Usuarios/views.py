from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from Usuarios.models import Avatar, Perfil
from Usuarios.forms import PerfilFormulario, AvatarFormulario, EditarUsuario, UserSearchForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

class RegistroVista(FormView):
    template_name = 'Usuarios\\registro.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('perfil')

    def form_valid(self, form):
        user = form.save()

        # Verificar si ya existe un Avatar para el usuario
        avatar = Avatar.objects.filter(user=user).first()
        if not avatar:
            avatar = Avatar.objects.create(user=user)
            avatar.image = None
            avatar.save()

        # Verificar si ya existe un Perfil para el usuario
        perfil = Perfil.objects.filter(user=user).first()
        if not perfil:
            perfil = Perfil.objects.create(user=user)
            perfil.fecha_nacimiento = None
            perfil.pais_nacimiento = None
            perfil.residencia = None
            perfil.institucion = None
            perfil.cargo = None

        login(self.request, user)
        return redirect(self.success_url)
    

class LoginVista(LoginView):
    template_name = 'Usuarios/login.html'

    def direccion_siguiente(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return super().get_success_url()

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect(self.direccion_siguiente())

@login_required
def LogoutVista(request):
    logout(request)
    return redirect(reverse_lazy("inicio"))

@login_required
def EditarPerfil(request):
    if Perfil.objects.filter(user=request.user).exists():
        perfil = request.user.perfil
    else:
        perfil = Perfil.objects.create(user=request.user)
    
    user = request.user

    if request.method == 'POST':
        if 'guardar_usuario' in request.POST:
            usuario_form = EditarUsuario(request.POST, instance=request.user)
            if usuario_form.is_valid():
                usuario = usuario_form.save(commit=False)

                # Verificar si los campos están vacíos y evitar sobreescribirlos
                if usuario_form.cleaned_data['username']:
                    usuario.username = usuario_form.cleaned_data['username']
                if usuario_form.cleaned_data['email']:
                    usuario.email = usuario_form.cleaned_data['email']
                if usuario_form.cleaned_data['first_name']:
                    usuario.first_name = usuario_form.cleaned_data['first_name']
                if usuario_form.cleaned_data['last_name']:
                    usuario.last_name = usuario_form.cleaned_data['last_name']

                usuario.save()
                return redirect(reverse_lazy('perfil'))

        elif 'guardar_perfil' in request.POST:
            perfil_form = PerfilFormulario(request.POST, instance=request.user.perfil)
            if perfil_form.is_valid():
                perfil = perfil_form.save(commit=False)

                # Verificar si los campos están vacíos y evitar sobreescribirlos
                if perfil_form.cleaned_data['fecha_nacimiento']:
                    perfil.fecha_nacimiento = perfil_form.cleaned_data['fecha_nacimiento']
                if perfil_form.cleaned_data['pais_nacimiento']:
                    perfil.pais_nacimiento = perfil_form.cleaned_data['pais_nacimiento']
                if perfil_form.cleaned_data['residencia']:
                    perfil.residencia = perfil_form.cleaned_data['residencia']
                if perfil_form.cleaned_data['institucion']:
                    perfil.institucion = perfil_form.cleaned_data['institucion']
                if perfil_form.cleaned_data['cargo']:
                    perfil.cargo = perfil_form.cleaned_data['cargo']

                perfil.save()
                return redirect(reverse_lazy('perfil'))

        elif 'subir_avatar' in request.POST:
            avatar_form = AvatarFormulario(request.POST, request.FILES)
            if avatar_form.is_valid():
                avatar = Avatar.objects.get(user=request.user)

                # Verificar si el campo de imagen no está vacío y evitar sobreescribirlo
                if avatar_form.cleaned_data['image']:
                    avatar.image = avatar_form.cleaned_data['image']

                avatar.save()
                return redirect(reverse_lazy('perfil'))

        return redirect(reverse_lazy('perfil')) 
    else:
        usuario_form = EditarUsuario(initial={
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name
        })
        perfil_form = PerfilFormulario(initial={
                'fecha_nacimiento': request.user.perfil.fecha_nacimiento,
                'pais_nacimiento': request.user.perfil.pais_nacimiento,
                'residencia': request.user.perfil.residencia,
                'institucion': request.user.perfil.institucion,
                'cargo': request.user.perfil.cargo,
                'pagina_web': request.user.perfil.pagina_web,
        })
        avatar_form = AvatarFormulario()


    context = {
        'usuario_form': usuario_form,
        'perfil_form': perfil_form,
        'avatar_form': avatar_form,
    }

    return render(request, "Usuarios\\perfil.html", context)

@login_required
def ver_perfil(request, username):
    user = request.user
    if user.username == username:
            return redirect(reverse_lazy('perfil'))
    else:
        try:
            usuario = User.objects.get(username=username)
            return render(request, 'Usuarios\\ver_perfil.html', {'usuario': usuario})
        except User.DoesNotExist:
            return render(request, 'Usuarios\\perfil_no_encontrado.html')



# import logging
# logger = logging.getLogger(__name__)

@login_required
def contribuyentes(request):
    # logger.info('entrando a la vista de contribuyentes')
    form = UserSearchForm()
    users = User.objects.all()

    if request.method == 'POST':
        form = UserSearchForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            institucion = form.cleaned_data['institucion']
            
            if username:
                users = users.filter(username__iexact=username)
                # logger.info(f'{users}')
            
            if first_name:
                users = users.filter(first_name__icontains=first_name)
                # logger.info(f'{users}')
            
            if last_name:
                users = users.filter(last_name__icontains=last_name)
                # logger.info(f'{users}')
            
            if institucion:
                users = users.filter(perfil__institucion__icontains=institucion)
                # logger.info(f'{users}')

    context = {'usuarios': users, 'form': form}
    return render(request, 'Usuarios/contribuyentes.html', context)


def cambiar_pass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '¡Tu contraseña ha sido cambiada exitosamente!')
            return redirect(reverse_lazy('perfil'))  # Redirige a la página de éxito
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = PasswordChangeForm(user=request.user)
    
    context = {'form': form}
    return render(request, 'Usuarios\\cambiar_contraseña.html', context)