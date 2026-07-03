from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import (
    CategoryViewSet,
    InventoryItemViewSet,
    OrderItemViewSet,
    OrderViewSet,
    ProductViewSet,
    SupplierViewSet,
)

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"suppliers", SupplierViewSet, basename="supplier")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"inventory-items", InventoryItemViewSet, basename="inventoryitem")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"order-items", OrderItemViewSet, basename="orderitem")

urlpatterns = [
    path("", include(router.urls)),
]
