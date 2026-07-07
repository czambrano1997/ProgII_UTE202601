from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (AutorViewSet, EditorialViewSet, CategoriaViewSet, 
                    LibroViewSet, PrestamoViewSet)

router = DefaultRouter()
router.register(r'autores', AutorViewSet, basename='autor')
router.register(r'editoriales', EditorialViewSet, basename='editorial')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'libros', LibroViewSet, basename='libro')
router.register(r'prestamos', PrestamoViewSet, basename='prestamo')

urlpatterns = [path('api/', include(router.urls))]