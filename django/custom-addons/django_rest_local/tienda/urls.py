from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoriaViewSet,
    ProductoViewSet,
    categoria_detail,
    categoria_list,
    home_view,
    producto_create,
    producto_detail,
    producto_list,
)


router = DefaultRouter()
router.register(r"productos", ProductoViewSet, basename="producto")
router.register(r"categorias", CategoriaViewSet, basename="categoria")

urlpatterns = [
    path("", home_view, name="home"),
    path("api/", include(router.urls)),
    path("productos/", producto_list, name="producto_list"),
    path("productos/nuevo/", producto_create, name="producto_create"),
    path("productos/<int:pk>/", producto_detail, name="producto_detail"),
    path("categorias/", categoria_list, name="categoria_list"),
    path("categorias/<int:pk>/", categoria_detail, name="categoria_detail"),
]