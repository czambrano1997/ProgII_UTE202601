from django.shortcuts import render
from .models import Categoria, Producto, Proveedor, FichaTecnica
from .models import Cliente, Pedido, DetallePedido, Bodega, Descuento

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import (
    CategoriaSerializer, ProveedorSerializer, FichaTecnicaSerializer, ProductoSerializer,
    ClienteSerializer, PedidoSerializer, DetallePedidoSerializer, BodegaSerializer,
    DescuentoSerializer,
)

# Funciones para vista categoria
def lista_categoria(request):
    categorias = Categoria.objects.all()
    contexto = {
        'carrera': 'PROGRAMACION II',
        'categorias': categorias,
        'total': categorias.count(),
    }
    return render(request, 'inventario/categoria.html', contexto)

# Funciones para vista productos
def lista_productos(request):
    productos = (
        Producto.objects
        .select_related('categoria', 'ficha_tecnica')  # FK y 1:1
        .prefetch_related('proveedores')                # N:M
        .all()
    )
    return render(request, 'inventario/producto.html', {'productos': productos})

# NUEVAS VISTAS
def lista_clientes(request):
    clientes = Cliente.objects.all()
    contexto = {
        'clientes': clientes,
        'total':    clientes.count(),
    }
    return render(request, 'inventario/cliente.html', contexto)


def lista_pedidos(request):
    pedidos = Pedido.objects.select_related('cliente').all()
    contexto = {
        'pedidos': pedidos,
        'total':   pedidos.count(),
    }
    return render(request, 'inventario/pedido.html', contexto)


def lista_detalles(request):
    detalles = DetallePedido.objects.select_related('pedido', 'producto').all()
    contexto = {
        'detalles': detalles,
        'total':    detalles.count(),
    }
    return render(request, 'inventario/detalle.html', contexto)


def lista_bodegas(request):
    bodegas = Bodega.objects.all()
    contexto = {
        'bodegas': bodegas,
        'total':   bodegas.count(),
    }
    return render(request, 'inventario/bodega.html', contexto)


def lista_descuentos(request):
    descuentos = Descuento.objects.select_related('producto').all()
    contexto = {
        'descuentos': descuentos,
        'total':      descuentos.count(),
    }
    return render(request, 'inventario/descuento.html', contexto)


#Apis
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
 
 
class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
 
 
class FichaTecnicaViewSet(viewsets.ModelViewSet):
    queryset = FichaTecnica.objects.all()
    serializer_class = FichaTecnicaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
 
 
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = (
        Producto.objects
        .select_related('categoria', 'ficha_tecnica')
        .prefetch_related('proveedores')
        .all()
    )
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
 
 
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
 
 
class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.select_related('cliente').all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
 
 
class DetallePedidoViewSet(viewsets.ModelViewSet):
    queryset = DetallePedido.objects.select_related('pedido', 'producto').all()
    serializer_class = DetallePedidoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
 
 
class BodegaViewSet(viewsets.ModelViewSet):
    queryset = Bodega.objects.all()
    serializer_class = BodegaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
 
 
class DescuentoViewSet(viewsets.ModelViewSet):
    queryset = Descuento.objects.select_related('producto').all()
    serializer_class = DescuentoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]