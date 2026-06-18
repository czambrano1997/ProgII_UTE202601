from django.shortcuts import render
from .models import Proveedor, Categoria, Producto, Cliente, Pedido

# 1. Vista de proveedor
def lista_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'djangov1/proveedores.html', {'proveedores': proveedores})

# 2. Vista de categoria
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'djangov1/categorias.html', {'categorias': categorias})

# 3. Vista de rpoducto
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'djangov1/productos.html', {'productos': productos})

# 4. Vista de cliente
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'djangov1/clientes.html', {'clientes': clientes})

# 5. Vista de edido
def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'djangov1/pedidos.html', {'pedidos': pedidos})
