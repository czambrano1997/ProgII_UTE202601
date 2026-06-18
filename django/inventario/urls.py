from django.urls import path
from . import views

app_name = "inventario"

urlpatterns = [
    path("", views.home, name="home"),
    path("categories/", views.category_list, name="category_list"),
    path("suppliers/", views.supplier_list, name="supplier_list"),
    path("products/", views.product_list, name="product_list"),
    path("inventory/", views.inventoryitem_list, name="inventoryitem_list"),
    path("orders/", views.order_list, name="order_list"),
    path("order-items/", views.orderitem_list, name="orderitem_list"),
]
