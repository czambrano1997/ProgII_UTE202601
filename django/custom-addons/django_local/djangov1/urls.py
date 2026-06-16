from django.urls import path
from .views import (
    CategoriaListView, 
    ProveedorListView, 
    ProductoListView, 
    ClienteListView, 
    VentaListView
)

urlpatterns = [
    path('categorias/', CategoriaListView.as_view(), name='categoria_list'),
    path('proveedores/', ProveedorListView.as_view(), name='proveedor_list'),
    path('productos/', ProductoListView.as_view(), name='producto_list'),
    path('clientes/', ClienteListView.as_view(), name='cliente_list'),
    path('ventas/', VentaListView.as_view(), name='venta_list'),
]