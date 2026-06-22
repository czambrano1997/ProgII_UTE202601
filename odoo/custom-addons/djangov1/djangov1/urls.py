from django.urls import path

from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('obras/', views.lista_obras, name='lista_obras'),
    path('obras/crear/', views.crear_obra, name='crear_obra'),
    path('actores/', views.lista_actores, name='lista_actores'),
    path('actores/crear/', views.crear_actor, name='crear_actor'),
    path('funciones/', views.lista_funciones, name='lista_funciones'),
    path('participaciones/', views.lista_participaciones, name='lista_participaciones'),
    path('boletos/', views.lista_boletos, name='lista_boletos'),
]
