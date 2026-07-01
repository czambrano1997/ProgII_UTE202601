
from django.shortcuts import render
from .models import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Genero, Artista, Disco, Cliente, Venta
from rest_framework import viewsets
from .serializers import(
    GeneroSerializer, ArtistaSerializer, DiscoSerializer, ClienteSerializer, VentaSerializer
    )


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


                
##views de api rest##

class GeneroViewSet(viewsets.ModelViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ArtistaViewSet(viewsets.ModelViewSet):
    queryset = Artista.objects.all()
    serializer_class = ArtistaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] 

class DiscoViewSet(viewsets.ModelViewSet):
    queryset = Disco.objects.all()
    serializer_class = DiscoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  

