from django.shortcuts import render, get_object_or_404

from .models import Category, Supplier, Product, InventoryItem, Order, OrderItem


def home(request):
    return render(request, "inventario/home.html")


def category_list(request):
	qs = Category.objects.all()
	return render(request, "inventario/category_list.html", {"object_list": qs})


def supplier_list(request):
	qs = Supplier.objects.all()
	return render(request, "inventario/supplier_list.html", {"object_list": qs})


def product_list(request):
	qs = Product.objects.select_related("category").all()
	return render(request, "inventario/product_list.html", {"object_list": qs})


def inventoryitem_list(request):
	qs = InventoryItem.objects.select_related("product").all()
	return render(request, "inventario/inventoryitem_list.html", {"object_list": qs})


def order_list(request):
	qs = Order.objects.select_related("supplier").all()
	return render(request, "inventario/order_list.html", {"object_list": qs})


def orderitem_list(request):
	qs = OrderItem.objects.select_related("order", "product").all()
	return render(request, "inventario/orderitem_list.html", {"object_list": qs})
