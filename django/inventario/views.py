from django.shortcuts import render, redirect, get_object_or_404

from .forms import CategoryForm, SupplierForm, ProductForm, InventoryItemForm, OrderForm, OrderItemForm
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


def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("inventario:category_list")
    return render(request, "inventario/form_page.html", {
        "form": form,
        "page_title": "Agregar categoría",
        "page_description": "Crea una nueva categoría para organizar tus productos.",
        "submit_text": "Guardar categoría",
    })


def supplier_create(request):
    form = SupplierForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("inventario:supplier_list")
    return render(request, "inventario/form_page.html", {
        "form": form,
        "page_title": "Agregar proveedor",
        "page_description": "Añade un nuevo proveedor con datos de contacto.",
        "submit_text": "Guardar proveedor",
    })


def product_create(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("inventario:product_list")
    return render(request, "inventario/form_page.html", {
        "form": form,
        "page_title": "Agregar producto",
        "page_description": "Registra un producto nuevo con categoría, precio y proveedores.",
        "submit_text": "Guardar producto",
    })


def inventoryitem_create(request):
    form = InventoryItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("inventario:inventoryitem_list")
    return render(request, "inventario/form_page.html", {
        "form": form,
        "page_title": "Agregar inventario",
        "page_description": "Agrega una entrada de inventario para un producto existente.",
        "submit_text": "Guardar inventario",
    })


def order_create(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("inventario:order_list")
    return render(request, "inventario/form_page.html", {
        "form": form,
        "page_title": "Agregar orden",
        "page_description": "Crea una nueva orden de compra con proveedor y total.",
        "submit_text": "Guardar orden",
    })


def orderitem_create(request):
    form = OrderItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("inventario:orderitem_list")
    return render(request, "inventario/form_page.html", {
        "form": form,
        "page_title": "Agregar item de orden",
        "page_description": "Añade un producto a una orden existente.",
        "submit_text": "Guardar item",
    })


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
