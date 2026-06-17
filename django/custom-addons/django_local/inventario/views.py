from django.shortcuts import render
from .models import Proveedor, Categoria, Producto, Cliente, RegistroVenta

def vista_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'inventario/provedores.html', {'datos': proveedores})

def vista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'inventario/categorias.html', {'datos': categorias})

def vista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'inventario/producto.html', {'datos': productos})

def vista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'inventario/clientes.html', {'datos': clientes})

def vista_ventas(request):
    ventas = RegistroVenta.objects.all()
    return render(request, 'inventario/ventas.html', {'datos': ventas})