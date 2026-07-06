from rest_framework.routers import DefaultRouter
from .viewsets import (
    CategoriaViewSet,
    ClienteViewSet,
    DetallePedidoViewSet,
    PedidoViewSet,
    ProductoViewSet,
)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'pedidos', PedidoViewSet, basename='pedido')
router.register(r'detalles-pedido', DetallePedidoViewSet, basename='detalle-pedido')

urlpatterns = router.urls
