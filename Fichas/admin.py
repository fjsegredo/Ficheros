from django.contrib import admin
from Fichas.models import Libro, Capitulo, Articulo, Ficha

class LibroAdmin(admin.ModelAdmin):
    readonly_fields = ('contribuyente', 'fecha_contribucion')

class CapituloAdmin(admin.ModelAdmin):
    readonly_fields = ('contribuyente', 'fecha_contribucion')

class ArticuloAdmin(admin.ModelAdmin):
    readonly_fields = ('contribuyente', 'fecha_contribucion')

class FichaAdmin(admin.ModelAdmin):
    readonly_fields = ('contribuyente', 'fecha_contribucion')


admin.site.register(Libro, LibroAdmin)
admin.site.register(Capitulo, CapituloAdmin)
admin.site.register(Articulo, ArticuloAdmin)
admin.site.register(Ficha, FichaAdmin)
