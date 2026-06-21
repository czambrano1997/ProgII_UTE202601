from django.shortcuts import render
from .models import Pelicula, Sala, Funcion, Cliente, Boleto
# Create your views here.


def ver_peliculas(request):
    datos = Pelicula.objects.all()
    return render(request, 'djangov1/peliculas.html', {'peliculas': datos})

def ver_salas(request):
    datos = Sala.objects.all()
    return render(request, 'djangov1/salas.html', {'salas': datos})

def ver_funciones(request):
    datos = Funcion.objects.all()
    return render(request, 'djangov1/funciones.html', {'funciones': datos})

def ver_clientes(request):
    datos = Cliente.objects.all()
    return render(request, 'djangov1/clientes.html', {'clientes': datos})

def ver_boletos(request):
    datos = Boleto.objects.all()
    return render(request, 'djangov1/boletos.html', {'boletos': datos})