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
    path('categoria/', views.lista_categoria, name='categoria'),
    path('producto/', views.lista_productos, name='lista_productos'),
    
 # Rutas nuevas
    path('cliente/',    views.lista_clientes,  name='lista_clientes'),
    path('pedido/',     views.lista_pedidos,   name='lista_pedidos'),
    path('detalle/',    views.lista_detalles,  name='lista_detalles'),
    path('bodega/',     views.lista_bodegas,   name='lista_bodegas'),
    path('descuento/',  views.lista_descuentos, name='lista_descuentos'),
]