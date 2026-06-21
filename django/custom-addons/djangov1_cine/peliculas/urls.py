from django.urls import path
from . import views

urlpatterns = [
    path('peliculas/', views.ver_peliculas),
    path('salas/', views.ver_salas),
    path('funciones/', views.ver_funciones),
    path('clientes/', views.ver_clientes),
    path('boletos/', views.ver_boletos),
]