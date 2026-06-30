from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import (
    Categoria,
    Proveedor,
    Producto,
    Cliente,
    Venta,
    DetalleVenta,
)
from .serializers import (
    CategoriaSerializer,
    ProveedorSerializer,
    ProductoSerializer,
    ClienteSerializer,
    VentaSerializer,
    DetalleVentaSerializer,
)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all().prefetch_related('detalles')
    serializer_class = VentaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]