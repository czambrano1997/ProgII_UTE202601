from django.shortcuts import render, get_object_or_404
from .models import Categoria, Proveedor, Producto, Almacen, EntradaStock


def lista_categorias(request):
    qs = Categoria.objects.all()
    return render(request, 'djangov1/categorias.html', {'categorias': qs})


def lista_proveedores(request):
    qs = Proveedor.objects.all()
    return render(request, 'djangov1/proveedores.html', {'proveedores': qs})


def lista_productos(request):
    qs = Producto.objects.select_related('categoria').all()
    return render(request, 'djangov1/productos.html', {'productos': qs})


def lista_almacenes(request):
    qs = Almacen.objects.all()
    return render(request, 'djangov1/almacenes.html', {'almacenes': qs})


def lista_entradas(request):
    qs = EntradaStock.objects.select_related('producto', 'almacen').all()
    return render(request, 'djangov1/entradas.html', {'entradas': qs})


def index_menu(request):
    # central menu page
    return render(request, 'djangov1/index.html')
