from django.urls import path
from . import views

app_name = 'djangov1'

urlpatterns = [
    path('', views.index_menu, name='index'),
    path('categorias/', views.lista_categorias, name='categorias'),
    path('proveedores/', views.lista_proveedores, name='proveedores'),
    path('productos/', views.lista_productos, name='productos'),
    path('almacenes/', views.lista_almacenes, name='almacenes'),
    path('entradas/', views.lista_entradas, name='entradas'),
]
