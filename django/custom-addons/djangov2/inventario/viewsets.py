from rest_framework import viewsets
from .models import Categoria, Cliente, DetallePedido, Pedido, Producto
from .serializers import (
    CategoriaSerializer,
    ClienteSerializer,
    DetallePedidoSerializer,
    PedidoSerializer,
    ProductoSerializer,
)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.select_related('categoria').all()
    serializer_class = ProductoSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.select_related('cliente').prefetch_related('detalles__producto').all()
    serializer_class = PedidoSerializer


class DetallePedidoViewSet(viewsets.ModelViewSet):
    queryset = DetallePedido.objects.select_related('pedido', 'producto').all()
    serializer_class = DetallePedidoSerializer
