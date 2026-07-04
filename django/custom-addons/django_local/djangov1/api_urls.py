from rest_framework import routers
from .views import (
    TipoFlorViewSet,
    ProveedorViewSet,
    FlorViewSet,
    ClienteViewSet,
    PedidoViewSet,
)

router = routers.DefaultRouter()

router.register(r'tiposflores', TipoFlorViewSet)
router.register(r'proveedores', ProveedorViewSet)
router.register(r'flores', FlorViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'pedidos', PedidoViewSet)

urlpatterns = router.urls