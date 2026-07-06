
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from djangov2 import views

router = DefaultRouter()
router.register(r'autores', views.AutorViewSet)
router.register(r'editoriales', views.EditorialViewSet)
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'libros', views.LibroViewSet)
router.register(r'prestamos', views.PrestamoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('autores/', views.autores_list, name='autores'),
    path('editoriales/', views.editoriales_list, name='editoriales'),
    path('categorias/', views.categorias_list, name='categorias'),
    path('libros/', views.libros_list, name='libros'),
    path('prestamos/', views.prestamos_list, name='prestamos'),
    path('api/', include(router.urls)),
]
