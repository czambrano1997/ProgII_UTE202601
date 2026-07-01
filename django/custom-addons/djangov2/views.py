from rest_framework import filters, viewsets

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
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nombre", "descripcion"]
    ordering_fields = ["id", "nombre", "creado_en"]


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.select_related("categoria").all()
    serializer_class = ProductoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nombre", "descripcion", "categoria__nombre"]
    ordering_fields = ["id", "nombre", "precio", "stock", "creado_en"]


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["cedula", "nombres", "apellidos", "email", "telefono"]
    ordering_fields = ["id", "apellidos", "nombres", "creado_en"]


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.select_related("cliente").prefetch_related("detalles__producto").all()
    serializer_class = PedidoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["cliente__nombres", "cliente__apellidos", "estado", "observacion"]
    ordering_fields = ["id", "fecha", "estado"]


class DetallePedidoViewSet(viewsets.ModelViewSet):
    queryset = DetallePedido.objects.select_related("pedido", "producto").all()
    serializer_class = DetallePedidoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["producto__nombre", "pedido__cliente__nombres", "pedido__cliente__apellidos"]
    ordering_fields = ["id", "cantidad", "precio_unitario"]
