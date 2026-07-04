from django.shortcuts import render
from rest_framework import viewsets
from peliculas.models import Pelicula,Sala,Funcion,Cliente,Boleto
from .serializers import (
    PeliculaSerializer,
    SalaSerializer,
    FuncionSerializer,
    ClienteSerializer,
    BoletoSerializer,
)

class PeliculaViewSet(viewsets.ModelViewSet):
    queryset = Pelicula.objects.all()
    serializer_class = PeliculaSerializer

class SalaViewSet(viewsets.ModelViewSet):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer

class FuncionViewSet(viewsets.ModelViewSet):
    queryset = Funcion.objects.all()
    serializer_class = FuncionSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    
class BoletoViewSet(viewsets.ModelViewSet):
    queryset = Boleto.objects.all()
    serializer_class = BoletoSerializer
    
    
       

