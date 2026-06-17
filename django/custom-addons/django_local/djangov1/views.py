from django.shortcuts import render
from .models import Autor, Categoria, Libro, Usuario, Prestamo

def autores(request):
    datos = Autor.objects.all()
    return render(request, 'autores.html', {'datos': datos})

def categorias(request):
    datos = Categoria.objects.all()
    return render(request, 'categorias.html', {'datos': datos})

def libros(request):
    datos = Libro.objects.all()
    return render(request, 'libros.html', {'datos': datos})

def usuarios(request):
    datos = Usuario.objects.all()
    return render(request, 'usuarios.html', {'datos': datos})

def prestamos(request):
    datos = Prestamo.objects.all()
    return render(request, 'prestamos.html', {'datos': datos})