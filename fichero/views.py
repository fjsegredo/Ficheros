from django.shortcuts import render

def inicio(request):
    return render(request, "inicio.html")

def about(request):
    return render(request, "about.html")