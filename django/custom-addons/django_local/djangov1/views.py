from rest_framework import viewsets

from .models import TipoFlor, Proveedor, Flor, Cliente, Pedido
from .serializers import (
    TipoFlorSerializer,
    ProveedorSerializer,
    FlorSerializer,
    ClienteSerializer,
    PedidoSerializer,
)


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