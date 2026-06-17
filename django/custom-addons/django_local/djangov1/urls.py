from django.urls import path
from . import views

urlpatterns = [
    path('autores/', views.autores, name='autores'),
    path('categorias/', views.categorias, name='categorias'),
    path('libros/', views.libros, name='libros'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('prestamos/', views.prestamos, name='prestamos'),
]