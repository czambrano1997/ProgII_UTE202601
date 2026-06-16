from django.shortcuts import render
from .models import Autor, CategoriaLibro, Libro, Cliente, Prestamo


def home(request):
    return render(request, 'djangov1/index.html')


def lista_autores(request):
    autores = Autor.objects.all()
    return render(request, 'djangov1/autor.html', {'autores': autores})


def lista_categorias(request):
    categorias = CategoriaLibro.objects.all()
    return render(request, 'djangov1/categoria.html', {'categorias': categorias})


def lista_libros(request):
    libros = Libro.objects.select_related('categoria').prefetch_related('autores').all()
    return render(request, 'djangov1/libro.html', {'libros': libros})


def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'djangov1/cliente.html', {'clientes': clientes})


def lista_prestamos(request):
    prestamos = Prestamo.objects.select_related('cliente', 'libro__categoria').all()
    return render(request, 'djangov1/prestamo.html', {'prestamos': prestamos})
