from django.urls import path

from .views import (
    CategoriaListView,
    ClienteListView,
    DetallePedidoListView,
    InicioView,
    PedidoListView,
    ProductoListView,
    ProveedorListView,
)


app_name = "djangov1"


urlpatterns = [
    path(
        "",
        InicioView.as_view(),
        name="inicio",
    ),
    path(
        "categorias/",
        CategoriaListView.as_view(),
        name="categorias",
    ),
    path(
        "proveedores/",
        ProveedorListView.as_view(),
        name="proveedores",
    ),
    path(
        "productos/",
        ProductoListView.as_view(),
        name="productos",
    ),
    path(
        "clientes/",
        ClienteListView.as_view(),
        name="clientes",
    ),
    path(
        "pedidos/",
        PedidoListView.as_view(),
        name="pedidos",
    ),
    path(
        "detalles-pedido/",
        DetallePedidoListView.as_view(),
        name="detalles_pedido",
    ),
]
