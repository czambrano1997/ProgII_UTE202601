from rest_framework.routers import DefaultRouter
from .views import (
    PeliculaViewSet,
    SalaViewSet,
    FuncionViewSet,
    ClienteViewSet,
    BoletoViewSet,
)

router = DefaultRouter()
router.register(r'peliculas', PeliculaViewSet)
router.register(r'salas', SalaViewSet)
router.register(r'funciones', FuncionViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'boletos', BoletoViewSet)

urlpatterns = router.urls