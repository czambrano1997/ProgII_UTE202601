from django.shortcuts import render

from .models import Autor, Editorial, Categoria, Libro, Prestamo


def autores_list(request):
    autores = Autor.objects.all()
    return render(request, 'djangov1/autores.html', {'autores': autores})


def editoriales_list(request):
    editoriales = Editorial.objects.all()
    return render(request, 'djangov1/editoriales.html', {'editoriales': editoriales})


def categorias_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'djangov1/categorias.html', {'categorias': categorias})


def libros_list(request):
    libros = Libro.objects.select_related('autor', 'editorial', 'categoria').all()
    return render(request, 'djangov1/libros.html', {'libros': libros})


def prestamos_list(request):
    prestamos = Prestamo.objects.select_related('libro').all()
    return render(request, 'djangov1/prestamos.html', {'prestamos': prestamos})
