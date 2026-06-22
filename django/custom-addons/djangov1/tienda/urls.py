from django.urls import path
from . import views

urlpatterns = [
    path('categorias/', views.categorias, name='categorias'),
    path('productos/', views.productos, name='productos'),
    path('clientes/', views.clientes, name='clientes'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('detallepedidos/', views.detallepedidos, name='detallepedidos'),
]
