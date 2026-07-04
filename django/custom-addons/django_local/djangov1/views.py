from django.shortcuts import render
from rest_framework import viewsets

from .models import TipoFlor, Proveedor, Flor, Cliente, Pedido
from .serializers import (
    TipoFlorSerializer,
    ProveedorSerializer,
    FlorSerializer,
    ClienteSerializer,
    PedidoSerializer,
)



def clientes(request):
    datos = Cliente.objects.all()
    return render(request, "clientes.html", {"datos": datos})


def flores(request):
    datos = Flor.objects.all()
    return render(request, "flores.html", {"datos": datos})


def proveedores(request):
    datos = Proveedor.objects.all()
    return render(request, "proveedores.html", {"datos": datos})


def tipo_flores(request):
    datos = TipoFlor.objects.all()
    return render(request, "tipo_flores.html", {"datos": datos})


def pedidos(request):
    datos = Pedido.objects.all()
    return render(request, "pedidos.html", {"datos": datos})




class TipoFlorViewSet(viewsets.ModelViewSet):
    queryset = TipoFlor.objects.all()
    serializer_class = TipoFlorSerializer


class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer


class FlorViewSet(viewsets.ModelViewSet):
    queryset = Flor.objects.all()
    serializer_class = FlorSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer