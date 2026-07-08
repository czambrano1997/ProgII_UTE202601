# from django.urls import path
# from . import views
# 
# app_name = 'inventario'
# 
# urlpatterns = [
    # path('categorias/', views.lista_categoria, name='categorias'),
# ]
# 

from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'inventario'

router = routers.DefaultRouter()
router.register(r'categorias', views.CategoriaViewSet, basename='api-categoria')
router.register(r'proveedores', views.ProveedorViewSet, basename='api-proveedor')
router.register(r'fichas-tecnicas', views.FichaTecnicaViewSet, basename='api-ficha-tecnica')
router.register(r'productos', views.ProductoViewSet, basename='api-producto')
router.register(r'clientes', views.ClienteViewSet, basename='api-cliente')
router.register(r'pedidos', views.PedidoViewSet, basename='api-pedido')
router.register(r'detalles', views.DetallePedidoViewSet, basename='api-detalle')
router.register(r'bodegas', views.BodegaViewSet, basename='api-bodega')
router.register(r'descuentos', views.DescuentoViewSet, basename='api-descuento')

urlpatterns = [
    path('categoria/', views.lista_categoria, name='categoria'),
    path('producto/', views.lista_productos, name='lista_productos'),
    path('cliente/', views.lista_clientes, name='lista_clientes'),
    path('pedido/', views.lista_pedidos, name='lista_pedidos'),
    path('detalle/', views.lista_detalles, name='lista_detalles'),
    path('bodega/', views.lista_bodegas, name='lista_bodegas'),
    path('descuento/', views.lista_descuentos, name='lista_descuentos'),


    path('api/', include(router.urls)),
]
 
#urlpatterns = [
#    path('categoria/', views.lista_categoria, name='categoria'),
#    path('producto/', views.lista_productos, name='lista_productos'),
#    
# Rutas nuevas
#    path('cliente/',    views.lista_clientes,  name='lista_clientes'),
#    path('pedido/',     views.lista_pedidos,   name='lista_pedidos'),
#    path('detalle/',    views.lista_detalles,  name='lista_detalles'),
#    path('bodega/',     views.lista_bodegas,   name='lista_bodegas'),
#    path('descuento/',  views.lista_descuentos, name='lista_descuentos'),
#]