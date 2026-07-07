from django.urls import path
from . import views

urlpatterns = [
    path('categorias/', views.categorias, name='categorias'),
    path('proveedores/', views.proveedores, name='proveedores'),
    path('platos/', views.platos, name='platos'),
    path('clientes/', views.clientes, name='clientes'),
    path('pedidos/', views.pedidos, name='pedidos'),
]