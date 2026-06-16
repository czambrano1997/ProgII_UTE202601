from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='djangov1_home'),
    path('autores/', views.lista_autores, name='lista_autores'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('libros/', views.lista_libros, name='lista_libros'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('prestamos/', views.lista_prestamos, name='lista_prestamos'),
]
