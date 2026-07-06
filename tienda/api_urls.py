from rest_framework.routers import DefaultRouter
from .api_views import (
    CategoriaViewSet,
    PlataformaViewSet,
    VideojuegoViewSet,
    ClienteViewSet,
    VentaViewSet,
)

router = DefaultRouter()

router.register(r'categorias', CategoriaViewSet)
router.register(r'plataformas', PlataformaViewSet)
router.register(r'videojuegos', VideojuegoViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'ventas', VentaViewSet)

urlpatterns = router.urls