from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from Fichas.models import Libro
from django import forms
from .models import Libro, Articulo, Capitulo, Ficha

class LibroFormulario(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'fecha_publicacion', 'etiqueta', 'ciudad_pais', 'editorial']

    def clean(self):
        cleaned_data = super().clean()

        # Limpiar y convertir a minúsculas los campos de texto
        for field_name in ['titulo', 'autor', 'etiqueta', 'ciudad_pais', 'editorial']:
            value = cleaned_data.get(field_name)
            if value:
                cleaned_data[field_name] = value.lower()

        return cleaned_data
    
class ArticuloFormulario(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['titulo', 'autor', 'publicacion', 'fecha_publicacion', 'etiqueta', 'volumen', 'numero', 'ciudad_pais', 'editorial', 'pagina_inicio', 'pagina_final',]
    
    def clean(self):
        cleaned_data = super().clean()

        # Limpiar y convertir a minúsculas los campos de texto
        for field_name in ['titulo', 'autor', 'publicacion', 'etiqueta', 'ciudad_pais', 'editorial']:
            value = cleaned_data.get(field_name)
            if value:
                cleaned_data[field_name] = value.lower()

        return cleaned_data

class CapituloFormulario(forms.ModelForm):
    class Meta:
        model = Capitulo
        fields = ['titulo_capitulo', 'autor_capitulo', 'fecha_publicacion', 'etiqueta', 'titulo', 'autor', 'pagina_inicio', 'pagina_final', 'ciudad_pais', 'editorial', ]
    
    def clean(self):
        cleaned_data = super().clean()

        # Limpiar y convertir a minúsculas los campos de texto
        for field_name in ['titulo', 'autor', 'etiqueta', 'ciudad_pais', 'editorial', 'titulo_capitulo', 'autor_capitulo']:
            value = cleaned_data.get(field_name)
            if value:
                cleaned_data[field_name] = value.lower()

        return cleaned_data

class FichaFormulario(forms.ModelForm):

    class Meta:
        model = Ficha
        exclude = ['contribuyente', 'fecha_contribucion', 'libro']

    def __init__(self, *args, **kwargs):
        super(FichaFormulario, self).__init__(*args, **kwargs)
        self.fields['imagen'].required = False

class BuscarLibrosFormulario(forms.Form):
    OPCIONES_BUSQUEDA = [
        ('titulo', 'Título'),
        ('autor', 'Autor'),
        ('fecha_publicacion', 'Año de publicación'),
        ('etiqueta', 'Etiqueta'),
        ('autor_capitulo', 'Autor del Capítulo'),
        ('titulo_capitulo', 'Título del Capítulo'),
    ]

    busqueda = forms.CharField(label='Buscar:', max_length=100, required=True)
    opcion = forms.ChoiceField(label='Según:', choices=OPCIONES_BUSQUEDA, required=True)

class SoloLibrosFormulario(forms.Form):
    titulo = forms.CharField(required=False)
    autor = forms.CharField(required=False)
    fecha_publicacion = forms.IntegerField(required=False)
    editorial = forms.CharField(required=False)

class SoloArticulosFormulario(forms.Form):
    titulo = forms.CharField(required=False)
    autor = forms.CharField(required=False)
    fecha_publicacion = forms.IntegerField(required=False)
    etiqueta = forms.CharField(required=False)

class SoloCapitulosFormulario(forms.Form):
    titulo_capitulo = forms.CharField(required=False)
    autor_capitulo = forms.CharField(required=False)
    titulo = forms.CharField(required=False)
    autor = forms.CharField(required=False)
    fecha_publicacion = forms.IntegerField(required=False)
    etiqueta = forms.CharField(required=False)

class BuscadorFichasFormulario(forms.Form):
    texto_buscar = forms.CharField(label='Texto a buscar', max_length=100, required=False)
    contribuyente = forms.CharField(label='Contribuyente', max_length=100, required=False)
    libro = forms.CharField(label='Libro', max_length=100, required=False)