from django.shortcuts import render
from .models import Categoria, Producto, Cliente, Pedido, DetallePedido

def categorias(request):
    datos = Categoria.objects.all()
    return render(request, 'categorias.html', {'datos': datos})

def productos(request):
    datos = Producto.objects.all()
    return render(request, 'productos.html', {'datos': datos})

def clientes(request):
    datos = Cliente.objects.all()
    return render(request, 'clientes.html', {'datos': datos})

def pedidos(request):
    datos = Pedido.objects.all()
    return render(request, 'pedidos.html', {'datos': datos})

def detallepedidos(request):
    datos = DetallePedido.objects.all()
    return render(request, 'detallepedidos.html', {'datos': datos})
