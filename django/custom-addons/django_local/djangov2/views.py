from django.shortcuts import render
from rest_framework import viewsets

from .models import Autor, Categoria, Libro, Usuario, Prestamo
from .serializers import (
    AutorSerializer,
    CategoriaSerializer,
    LibroSerializer,
    UsuarioSerializer,
    PrestamoSerializer,
)


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


class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class PrestamoViewSet(viewsets.ModelViewSet):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer