from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from Fichas.forms import BuscadorFichasFormulario, SoloLibrosFormulario, SoloArticulosFormulario, SoloCapitulosFormulario, LibroFormulario, ArticuloFormulario, CapituloFormulario, FichaFormulario, BuscarLibrosFormulario
from Fichas.models import Libro, Capitulo, Articulo, Ficha
from django.db.models import Q
from django.contrib.auth.models import User


####LIBROS####

@login_required
def agregar_libro(request):
    if request.method == 'POST':
        form = LibroFormulario(request.POST)
        if form.is_valid():
            libro = form.save(commit=False)
            libro.contribuyente = request.user
            libro.save()
            return redirect(reverse_lazy('inicio'))  # REDIRIGIR A FICHAR LIBRO
    else:
        form = LibroFormulario()

    return render(request, 'Fichas\\agregar_libro.html', {'form': form})

def libros(request):
    if request.method == 'POST':
        formulario = SoloLibrosFormulario(request.POST)
        if formulario.is_valid():
            titulo = formulario.cleaned_data['titulo']
            autor = formulario.cleaned_data['autor']
            fecha_publicacion = formulario.cleaned_data['fecha_publicacion']
            editorial = formulario.cleaned_data['editorial']
            if titulo:                    
                libros = Libro.objects.exclude(Q(articulo__isnull=False) | Q(capitulo__isnull=False)).filter(titulo__icontains=titulo).order_by('titulo')
            if autor:        
                libros = Libro.objects.exclude(Q(articulo__isnull=False) | Q(capitulo__isnull=False)).filter(autor__icontains=autor).order_by('titulo')
            if fecha_publicacion:
                libros = Libro.objects.exclude(Q(articulo__isnull=False) | Q(capitulo__isnull=False)).filter(fecha_publicacion=fecha_publicacion).order_by('titulo')
            if editorial:
                libros = Libro.objects.exclude(Q(articulo__isnull=False) | Q(capitulo__isnull=False)).filter(editorial__icontains=editorial).order_by('titulo')
    else:
        formulario = SoloLibrosFormulario()
        libros = Libro.objects.exclude(Q(articulo__isnull=False) | Q(capitulo__isnull=False)).order_by('titulo')
    
    context = {'libros': libros, 'formulario': formulario}
    return render(request, 'Fichas\\libros.html', context)

@login_required
def ver_libro(request, id):
    try:
        libro = Libro.objects.get(id=id)
        if isinstance(libro, Articulo):
            libro = Libro.objects.get(id=id)
            request.session['id'] = libro.id
            return redirect(reverse_lazy("ver_articulo"))
        elif isinstance(libro, Capitulo):
            libro = Capitulo.objects.get(id=id)
            request.session['id'] = id
            return redirect(reverse_lazy("ver_capitulo"))
        else:
            return render(request, "Fichas/ver_libro.html", {'libro': libro})
    except Libro.DoesNotExist: 
        return render(request, "Fichas/libro_no_encontrado.html")
    

###ARTICULOS####

def articulos(request):
    if request.method == 'POST':
        formulario = SoloArticulosFormulario(request.POST)
        if formulario.is_valid():
            titulo = formulario.cleaned_data['titulo']
            autor = formulario.cleaned_data['autor']
            fecha_publicacion = formulario.cleaned_data['fecha_publicacion']
            etiqueta = formulario.cleaned_data['etiqueta']
            articulos = Articulo.objects.filter(etiqueta__icontains=etiqueta).order_by('titulo')
            
            if titulo:
                articulos = articulos.filter(titulo__icontains=titulo)
            if autor:
                articulos = articulos.filter(autor__icontains=autor)
            if fecha_publicacion:
                articulos = articulos.filter(fecha_publicacion=fecha_publicacion)
        else:
            articulos = Articulo.objects.all().order_by('titulo')
    else:
        formulario = SoloArticulosFormulario()
        articulos = Articulo.objects.all().order_by('titulo')
    
    context = {'articulos': articulos, 'formulario': formulario}
    return render(request, 'Fichas\\articulos.html', context)


@login_required
def ver_articulo(request, id):
    try:
        articulo = Articulo.objects.get(id=id)
        return render(request, "Fichas\\ver_articulo.html", {'articulo': articulo})
    except Articulo.DoesNotExist: 
        return render(request, "Fichas\\articulo_no_encontrado.html")
    
@login_required    
def agregar_articulo(request):
    if request.method == 'POST':
        form = ArticuloFormulario(request.POST)
        if form.is_valid():
            articulo = form.save(commit=False)
            articulo.contribuyente = request.user
            articulo.save()
            return redirect(reverse('ver_articulo', args=[articulo.id]))
    else:
        form = ArticuloFormulario()
    return render(request, 'Fichas\\agregar_articulo.html', {'form': form})

####CAPITULOS####

def capitulos(request):
    if request.method == 'POST':
        formulario = SoloCapitulosFormulario(request.POST)
        if formulario.is_valid():
            titulo_capitulo = formulario.cleaned_data['titulo_capitulo']
            autor_capitulo = formulario.cleaned_data['autor_capitulo']
            titulo = formulario.cleaned_data['titulo']
            autor = formulario.cleaned_data['autor']
            fecha_publicacion = formulario.cleaned_data['fecha_publicacion']
            etiqueta = formulario.cleaned_data['etiqueta']
            
            capitulos = Capitulo.objects.filter(etiqueta__icontains=etiqueta).order_by('titulo')
            
            if titulo_capitulo:
                capitulos = capitulos.filter(titulo_capitulo__icontains=titulo_capitulo)
            if autor_capitulo:
                capitulos = capitulos.filter(autor_capitulo__icontains=autor_capitulo)
            if titulo:
                capitulos = capitulos.filter(titulo__icontains=titulo)
            if autor:
                capitulos = capitulos.filter(autor__icontains=autor)
            if fecha_publicacion:
                capitulos = capitulos.filter(fecha_publicacion=fecha_publicacion)
        else:
            capitulos = Capitulo.objects.all().order_by('titulo')
    else:
        formulario = SoloCapitulosFormulario()
        capitulos = Capitulo.objects.all().order_by('titulo')
    
    context = {'capitulos': capitulos, 'formulario': formulario}
    return render(request, 'Fichas\\capitulos.html', context)



@login_required
def ver_capitulo(request, id):
    try:
        capitulo = Capitulo.objects.get(id=id)
        return render(request, "Fichas\\ver_capitulo.html", {'capitulo': capitulo})
    except Capitulo.DoesNotExist: 
        return render(request, "Fichas\\capitulo_no_encontrado.html")
    
@login_required    
def agregar_capitulo(request):
    if request.method == 'POST':
        form = CapituloFormulario(request.POST)
        if form.is_valid():
            capitulo = form.save(commit=False)
            capitulo.contribuyente = request.user
            capitulo.save()
            return redirect(reverse('ver_capitulo', args=[capitulo.id]))
    else:
        form = CapituloFormulario()
    return render(request, 'Fichas\\agregar_capitulo.html', {'form': form})

# # # # FICHAS


@login_required
def CrearFicha(request, id):
    if request.method == 'POST':
        form = FichaFormulario(request.POST, request.FILES)
        if form.is_valid():
            ficha = form.save(commit=False)
            ficha.contribuyente = request.user
            ficha.libro = Libro.objects.get(id=id)
            
            if 'imagen' in request.FILES:
                ficha.imagen = request.FILES['imagen']
            
            ficha.save()
            return redirect(reverse('ver_libro', args=[id]))
    else:
        libro = Libro.objects.get(id=id)
        libro_id = libro.id
        form = FichaFormulario()
    
    return render(request, 'Fichas\\crear_ficha.html', {'form': form, 'libro_id': libro_id, 'libro': libro})



@login_required
def fichas_por_libro(request, libro_id):
    libro = Libro.objects.get(id=libro_id)
    if isinstance(libro, Capitulo):
        titulo_capitulo = libro.titulo_capitulo
        autor_capitulo = libro.autor_capitulo
        context = {
            'titulo_capitulo': titulo_capitulo,
            'autor_capitulo': autor_capitulo,
        }
    else:
        context = {}

    fichas = Ficha.objects.filter(libro=libro)
    context.update({
        'fichas': fichas,
        'libro_id': libro.id,
        'titulo_libro': libro.titulo,
        'autor_libro': libro.autor,
    })

    return render(request, 'Fichas/fichas_por_libro.html', context)
from django.contrib.auth.models import User

def buscar_fichas(request):
    fichas = Ficha.objects.none()
    if request.method == 'POST':
        form = BuscadorFichasFormulario(request.POST)
        if form.is_valid():
            texto_buscar = form.cleaned_data['texto_buscar']
            username = form.cleaned_data['contribuyente']
            libro = form.cleaned_data['libro']
            
            fichas = Ficha.objects.all()
            
            if texto_buscar:
                fichas = fichas.filter(texto__icontains=texto_buscar)
            
            if username:
                fichas = fichas.filter(contribuyente__username__icontains=username)
            
            if libro:
                fichas = fichas.filter(libro__titulo__icontains=libro)
            
            context = {'fichas': fichas, 'form': form}
            return render(request, 'Fichas\\buscar_fichas.html', context)
    else:
        form = BuscadorFichasFormulario()

    context = {'form': form}
    return render(request, 'Fichas\\buscar_fichas.html', context)






## BUSQUEDA
def buscar_libros(request):
    form = BuscarLibrosFormulario(request.GET)
    resultados = None
    busqueda = None
    opcion = None

    if form.is_valid():
        busqueda = form.cleaned_data['busqueda']
        opcion = form.cleaned_data['opcion']

        if opcion == 'titulo':
            opcion = 'título'
            resultados = Libro.objects.filter(titulo__icontains=busqueda)
        elif opcion == 'autor':
            opcion = 'autor'
            resultados = Libro.objects.filter(autor__icontains=busqueda)
        elif opcion == 'fecha_publicacion':
            opcion = 'año de publicación'
            resultados = Libro.objects.filter(fecha_publicacion=int(busqueda))
        elif opcion == 'etiqueta':
            opcion = 'etiqueta o palabra clave'
            resultados = Libro.objects.filter(etiqueta__icontains=busqueda)
        elif opcion == 'autor_capitulo':
            opcion = 'autor del capítulo'
            resultados = Capitulo.objects.filter(autor_capitulo__icontains=busqueda)
        elif opcion == 'titulo_capitulo':
            opcion = 'autor_capitulo'
            resultados = Capitulo.objects.filter(titulo_capitulo__icontains=busqueda)

    return render(request, 'Fichas\\buscar_libros.html', {'form': form, 'busqueda': busqueda, 'resultados': resultados, 'opcion': opcion})

