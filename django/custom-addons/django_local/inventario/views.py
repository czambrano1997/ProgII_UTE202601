from django.shortcuts import render
from .models import *

# Create your views here.
def lista_generos(request):
    generos = Genero.objects.all()
    return render(request, 'inventario/genero.html', {'generos': generos})

def lista_artistas(request):
    artistas = Artista.objects.all()
    return render(request, 'inventario/artista.html',{'artistas':artistas})

def lista_discos(request):
    discos = Disco.objects.all()
    return render(request,'inventario/disco.html',{'discos':discos})

def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request,'inventario/cliente.html',{'clientes':clientes})

def lista_ventas(request):
    ventas =  Venta.objects.all()
    return render(request,'inventario/cliente.html',{'ventas':ventas})


                
