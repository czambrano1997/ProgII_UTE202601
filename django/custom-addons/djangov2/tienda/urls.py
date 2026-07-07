from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet,
    ClienteViewSet,
    DetallePedidoViewSet,
    PedidoViewSet,
    ProductoViewSet,
)

router = DefaultRouter()
router.register(r"productos", ProductoViewSet, basename="producto")
router.register(r"clientes", ClienteViewSet, basename="cliente")
router.register(r"categorias", CategoriaViewSet, basename="categoria")
router.register(r"pedidos", PedidoViewSet, basename="pedido")
router.register(r"detalle-pedidos", DetallePedidoViewSet, basename="detallepedido")

urlpatterns = [
    path("", include(router.urls)),
]
