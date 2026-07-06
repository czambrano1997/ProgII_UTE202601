"""
URL configuration for djangov1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
