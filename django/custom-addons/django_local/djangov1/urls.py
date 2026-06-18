from django.urls import path
from . import views


urlpatterns = [
    path('clientes/', views.clientes, name = 'clientes'),
    path('flores/', views.flores, name = 'flores'),
    path('pedidos/', views.pedidos, name = 'pedidos'),
    path('proveedores/', views.proveedores, name = 'proveedores'),
    path('tipo_flores/', views.tipo_flores, name = 'tipo_flores'),
]