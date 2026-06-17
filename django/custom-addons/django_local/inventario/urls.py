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
    path('proveedores/', views.vista_proveedores, name='proveedores'),
    path('categorias/', views.vista_categorias, name='categorias'),
    path('productos/', views.vista_productos, name='productos'),
    path('clientes/', views.vista_clientes, name='clientes'),
    path('ventas/', views.vista_ventas, name='ventas'),
]