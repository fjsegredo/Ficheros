from django import forms
from Usuarios.models import Avatar, Perfil
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()  # Agregar el campo de correo electrónico

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class AvatarFormulario(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['image',]
        labels = {'image': 'Sube un archivo. Generalmente se ven mejor las imágenes cuadradas sin transparencia, pero puedes experimentar ;):'}

class PerfilFormulario(forms.ModelForm):
    fecha_nacimiento = forms.DateField(label='Fecha de nacimiento (DD/MM/AA):', required=False)
    pais_nacimiento = forms.CharField(label='País de nacimiento:', required=False)
    residencia = forms.CharField(label='Lugar de residencia (Ciudad o País):', required=False)
    institucion = forms.CharField(label='Institución a la que pertenece (dejar en blanco si no corresponde):', required=False)
    cargo = forms.CharField(label='Cargo que tiene en la institución (dejar en blanco si no corresponde):', required=False)
    pagina_web = forms.URLField(label='Ingrese una url:', required=False)
    class Meta:
        model = Perfil
        fields = ['fecha_nacimiento', 'pais_nacimiento', 'residencia', 'institucion', 'cargo', 'pagina_web']

class EditarUsuario(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
        
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class UserSearchForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', required=False)
    first_name = forms.CharField(label='Nombre', required=False)
    last_name = forms.CharField(label='Apellido', required=False)
    institucion = forms.CharField(label='Institución', required=False)