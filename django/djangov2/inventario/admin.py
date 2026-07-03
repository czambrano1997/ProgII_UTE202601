from django.contrib import admin
from .models import Category, Supplier, Product, InventoryItem, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "created_at")


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "email", "phone", "active")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "sku", "price", "category", "active")
	list_filter = ("category", "active")


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
	list_display = ("id", "product", "quantity", "location", "last_updated")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ("id", "supplier", "date", "total")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	list_display = ("id", "order", "product", "quantity", "price")
