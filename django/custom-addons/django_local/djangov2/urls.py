from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'autores', views.AutorViewSet)
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'libros', views.LibroViewSet)
router.register(r'usuarios', views.UsuarioViewSet)
router.register(r'prestamos', views.PrestamoViewSet)

urlpatterns = [
    path('autores/', views.autores, name='autores'),
    path('categorias/', views.categorias, name='categorias'),
    path('libros/', views.libros, name='libros'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('prestamos/', views.prestamos, name='prestamos'),
    path('api/', include(router.urls)),
]