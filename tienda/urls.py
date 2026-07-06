from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("categorias/", views.categorias, name="categorias"),
    path("plataformas/", views.plataformas, name="plataformas"),
    path("videojuegos/", views.videojuegos, name="videojuegos"),
    path("clientes/", views.clientes, name="clientes"),
    path("ventas/", views.ventas, name="ventas"),
]