from django.db import models
from django.views.generic import ListView, TemplateView

from .models import Categoria, Cliente, DetallePedido, Pedido, Producto, Proveedor


class InicioView(TemplateView):
    template_name = "djangov1/inicio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "total_categorias": Categoria.objects.count(),
                "total_proveedores": Proveedor.objects.count(),
                "total_productos": Producto.objects.count(),
                "total_clientes": Cliente.objects.count(),
                "total_pedidos": Pedido.objects.count(),
                "productos_stock_bajo": Producto.objects.filter(
                    stock__lte=models.F("stock_minimo")
                ).count(),
            }
        )
        return context


class CategoriaListView(ListView):
    model = Categoria
    template_name = "djangov1/categorias.html"
    context_object_name = "categorias"


class ProveedorListView(ListView):
    model = Proveedor
    template_name = "djangov1/proveedores.html"
    context_object_name = "proveedores"


class ProductoListView(ListView):
    model = Producto
    template_name = "djangov1/productos.html"
    context_object_name = "productos"

    def get_queryset(self):
        return Producto.objects.select_related("categoria", "proveedor")


class ClienteListView(ListView):
    model = Cliente
    template_name = "djangov1/clientes.html"
    context_object_name = "clientes"


class PedidoListView(ListView):
    model = Pedido
    template_name = "djangov1/pedidos.html"
    context_object_name = "pedidos"

    def get_queryset(self):
        return Pedido.objects.select_related("cliente").prefetch_related("detalles__producto")


class DetallePedidoListView(ListView):
    model = DetallePedido
    template_name = "djangov1/detalles_pedido.html"
    context_object_name = "detalles"

    def get_queryset(self):
        return DetallePedido.objects.select_related("pedido", "producto", "pedido__cliente")


