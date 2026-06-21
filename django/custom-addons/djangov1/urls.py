from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_Home, name='home_futbol'),
    path('cliente/', views.vista_Clientes, name='clientes_futbol'),
    path('reserva/', views.vista_Reservas, name='hacer_reservas'),
    path('paquete/', views.vista_paquetes, name='paquetes_futbol'),
    path('inventario/', views.vista_Inventario, name='inventario_canchas'),
    path('gestion_reserva/', views.vista_Gestion, name='gestionar_reservas'),
    path('consumo/', views.vista_detalle_del_consumo, name='consumo_cliente'),
]