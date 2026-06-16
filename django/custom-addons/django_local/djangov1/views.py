from django.views.generic import ListView
from .models import Categoria, Proveedor, Producto, Cliente, Venta

class CategoriaListView(ListView):
    model = Categoria
    template_name = 'djangov1/categoria_list.html'
    context_object_name = 'categorias'

class ProveedorListView(ListView):
    model = Proveedor
    template_name = 'djangov1/proveedor_list.html'
    context_object_name = 'proveedores'

class ProductoListView(ListView):
    model = Producto
    template_name = 'djangov1/producto_list.html'
    context_object_name = 'productos'

class ClienteListView(ListView):
    model = Cliente
    template_name = 'djangov1/cliente_list.html'
    context_object_name = 'clientes'

class VentaListView(ListView):
    model = Venta
    template_name = 'djangov1/venta_list.html'
    context_object_name = 'ventas'