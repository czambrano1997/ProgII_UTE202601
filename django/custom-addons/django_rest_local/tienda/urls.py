from django.urls import path
from .views import (
    actualizar_producto,
    crear_producto,
    detalle_producto,
    eliminar_producto,
    lista_productos,
)

urlpatterns = [
    path("api/productos/", lista_productos, name="lista_productos"),
    path("api/productos/crear/", crear_producto, name="crear_producto"),
    path("api/productos/<int:pk>/", detalle_producto, name="detalle_producto"),
    path("api/productos/actualizar/<int:pk>/", actualizar_producto, name="actualizar_producto"),
    path("api/productos/eliminar/<int:pk>/", eliminar_producto, name="eliminar_producto"),
]