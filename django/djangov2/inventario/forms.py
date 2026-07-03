from django import forms

from .models import Category, Supplier, Product, InventoryItem, Order, OrderItem


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "email", "phone", "address", "active"]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "sku", "description", "price", "category", "suppliers", "active"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "suppliers": forms.SelectMultiple(attrs={"size": 6}),
        }


class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ["product", "quantity", "location"]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["supplier", "date", "total", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["order", "product", "quantity", "price"]
