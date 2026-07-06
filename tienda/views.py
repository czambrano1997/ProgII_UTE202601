from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Categoria, Plataforma, Videojuego, Cliente, Venta

def categorias(request):
    datos = Categoria.objects.all()
    return render(request, 'categorias.html', {'datos': datos})

def plataformas(request):
    datos = Plataforma.objects.all()
    return render(request, 'plataformas.html', {'datos': datos})

def videojuegos(request):
    datos = Videojuego.objects.all()
    return render(request, 'videojuegos.html', {'datos': datos})

def clientes(request):
    datos = Cliente.objects.all()
    return render(request, 'clientes.html', {'datos': datos})

def ventas(request):
    datos = Venta.objects.all()
    return render(request, 'ventas.html', {'datos': datos}) 

def inicio(request):
    return render(request, "inicio.html")

