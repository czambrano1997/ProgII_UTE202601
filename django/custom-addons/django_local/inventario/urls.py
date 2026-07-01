from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    GeneroViewSet, ArtistaViewSet, DiscoViewSet,
    ClienteViewSet, VentaViewSet
)

app_name = 'inventario'

urlpatterns = [
    path('generos/', views.lista_generos, name='generos'),
    path('artistas/', views.lista_artistas, name ='artistas'),
    path('discos/', views.lista_discos,name='discos'),
    path('clientes/',views.lista_clientes, name = 'clientes'),
    path('ventas/',views.lista_ventas, name = 'ventas'),
]



#rutas de api rest

router = DefaultRouter()
router.register(r'generos', GeneroViewSet)
router.register(r'artistas',ArtistaViewSet)
router.register(r'discos', DiscoViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'ventas', VentaViewSet)


urlpatterns += [
    path('api/', include(router.urls)),
]


