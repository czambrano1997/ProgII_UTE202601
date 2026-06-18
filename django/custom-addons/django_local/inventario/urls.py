# from django.urls import path
# from . import views
# 
# app_name = 'inventario'
# 
# urlpatterns = [
    # path('categorias/', views.lista_categoria, name='categorias'),
# ]
# 
from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('generos/', views.lista_generos, name='generos'),
    path('artistas/', views.lista_artistas, name ='artistas'),
    path('discos/', views.lista_discos,name='discos'),
    path('clientes/',views.lista_clientes, name = 'clientes'),
    path('ventas',views.lista_ventas, name = 'ventas'),
]