from django.urls import path
from . import views

app_name = "inventario"

urlpatterns = [
    path("", views.home, name="home"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/add/", views.category_create, name="category_create"),
    path("suppliers/", views.supplier_list, name="supplier_list"),
    path("suppliers/add/", views.supplier_create, name="supplier_create"),
    path("products/", views.product_list, name="product_list"),
    path("products/add/", views.product_create, name="product_create"),
    path("inventory/", views.inventoryitem_list, name="inventoryitem_list"),
    path("inventory/add/", views.inventoryitem_create, name="inventoryitem_create"),
    path("orders/", views.order_list, name="order_list"),
    path("orders/add/", views.order_create, name="order_create"),
    path("order-items/", views.orderitem_list, name="orderitem_list"),
    path("order-items/add/", views.orderitem_create, name="orderitem_create"),
]
