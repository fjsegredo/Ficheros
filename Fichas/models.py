from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
import os, uuid
from PIL import Image


def validar_publicacion(valor):
    if valor != 0 and (valor < 1500 or valor > 2200):
        raise ValidationError('El año de publicación debe estar entre 1500 y 2200. Busque otro año, como el año de la traducción o la edición. Ingrese "0" en caso de no conocerlo.')

# # # # LIBROS

class Libro(models.Model):
    titulo = models.CharField(max_length=300)
    autor = models.CharField(max_length=200)
    contribuyente = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_contribucion = models.DateTimeField(auto_now_add=True)
    fecha_publicacion = models.IntegerField(validators=[validar_publicacion])
    etiqueta = models.CharField(max_length=80, blank=True)
    ciudad_pais = models.CharField(max_length=100, blank=True)
    editorial = models.CharField(max_length=100, blank=True)

    def __str__(self):
        if self.es_articulo():
            return self.articulo.__str__()  # Devuelve el método __str__() de la clase Articulo
        elif self.es_capitulo():
            return self.capitulo.__str__()  # Devuelve el método __str__() de la clase Capitulo
        else:
            return f"({self.autor}) - {self.titulo}"

    def es_articulo(self):
        return hasattr(self, 'articulo')

    def es_capitulo(self):
        return hasattr(self, 'capitulo')

    
class Articulo(Libro):
    pagina_inicio = models.IntegerField()
    pagina_final = models.IntegerField()
    publicacion = models.CharField(max_length=200)
    volumen = models.CharField(max_length=4, validators=[RegexValidator(r'^[a-zA-Z0-9]{1,4}$', 'El volumen debe tener máximo 4 dígitos.')])
    numero = models.IntegerField()

    def __str__(self):
        return f"({self.autor}) - {self.titulo} | En: {self.publicacion} Año: {self.fecha_publicacion} Volumen: {self.volumen} | Número: {self.numero}"

    @staticmethod
    def validar_paginas(pagina_inicio, pagina_final):
        if pagina_inicio > pagina_final:
            raise ValidationError('La página inicial debe ser menor o igual a la página final.')

    def clean(self):
        self.validar_paginas(self.pagina_inicio, self.pagina_final)

class Capitulo(Libro):
    titulo_capitulo = models.CharField(max_length=300)
    autor_capitulo = models.CharField(max_length=200)
    pagina_inicio = models.IntegerField()
    pagina_final = models.IntegerField()

    @staticmethod
    def validar_paginas(pagina_inicio, pagina_final):
        if pagina_inicio > pagina_final:
            raise ValidationError('La página inicial debe ser menor o igual a la página final.')

    def clean(self):
        self.validar_paginas(self.pagina_inicio, self.pagina_final)

    def __str__(self):
        return f"({self.autor_capitulo}) - {self.titulo_capitulo} | {self.fecha_publicacion} en: {self.autor}, {self.titulo}"



def ficha_path(instance, filename):
    unique_filename = f"{uuid.uuid4()}{os.path.splitext(filename)[1]}"
    return os.path.join('fichas', unique_filename)


class Ficha(models.Model):
    contribuyente = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, null=False)
    fecha_contribucion = models.DateTimeField(auto_now_add=True)
    texto = models.TextField(max_length=10000)
    imagen = models.ImageField(upload_to=ficha_path, null=True)

    def __str__(self):
        return f'{self.contribuyente} - {self.libro} - {self.fecha_contribucion} '

    @property
    def es_foto(self):
        return hasattr(self, 'imagen')


