from django.urls import path
from . import views

urlpatterns = [
    path('proveedores/', views.lista_proveedores, name='lista_proveedores'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
]