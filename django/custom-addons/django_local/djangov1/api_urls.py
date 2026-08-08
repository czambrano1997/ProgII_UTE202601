from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet,
    ProveedorViewSet,
    PlatoViewSet,
    ClienteViewSet,
    PedidoViewSet,
)

router = DefaultRouter()

router.register(r'categorias', CategoriaViewSet)
router.register(r'proveedores', ProveedorViewSet)
router.register(r'platos', PlatoViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'pedidos', PedidoViewSet)

urlpatterns = router.urls