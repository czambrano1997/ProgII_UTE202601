from django.urls import path
from . import views
from rest_framework import routers
from . import api_views

router = routers.DefaultRouter()
router.register(r'clientes', api_views.ClienteViewSet)
router.register(r'reservas', api_views.ReservaViewSet)
router.register(r'paquetes', api_views.PaqueteViewSet)
router.register(r'inventario', api_views.InventarioViewSet)
router.register(r'canchas', api_views.CanchasViewSet)

urlpatterns = [
    path('', views.vista_Home, name='home_futbol'),
    path('cliente/', views.vista_Clientes, name='clientes_futbol'),
    path('reserva/', views.vista_Reservas, name='hacer_reservas'),
    path('paquete/', views.vista_paquetes, name='paquetes_futbol'),
    path('inventario/', views.vista_Inventario, name='inventario_canchas'),
    path('gestion_reserva/', views.vista_Gestion, name='gestionar_reservas'),
    path('consumo/', views.vista_detalle_del_consumo, name='consumo_cliente'),
]

# API routes
urlpatterns += router.urls
]