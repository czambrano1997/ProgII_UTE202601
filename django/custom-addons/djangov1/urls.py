from django.urls import path
from . import views

urlpatterns = [
    path('categorias/', views.lista_categorias, name='djangov1_categorias'),
    path('proveedores/', views.lista_proveedores, name='djangov1_proveedores'),
    path('productos/', views.lista_productos, name='djangov1_productos'),
    path('almacenes/', views.lista_almacenes, name='djangov1_almacenes'),
    path('entradas/', views.lista_entradas, name='djangov1_entradas'),
]
