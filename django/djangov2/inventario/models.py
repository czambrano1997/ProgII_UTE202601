from django.db import models
from decimal import Decimal


class Category(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class Supplier(models.Model):
	name = models.CharField(max_length=150)
	email = models.EmailField(blank=True)
	phone = models.CharField(max_length=30, blank=True)
	address = models.TextField(blank=True)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.name


class Product(models.Model):
	name = models.CharField(max_length=200)
	sku = models.CharField(max_length=50, unique=True)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
	suppliers = models.ManyToManyField(Supplier, blank=True, related_name='products')
	active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.name} ({self.sku})"


class InventoryItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory_items')
	quantity = models.IntegerField()
	location = models.CharField(max_length=100, blank=True)
	last_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.product.name} — {self.quantity}"


class Order(models.Model):
	supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='orders')
	date = models.DateField()
	total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
	products = models.ManyToManyField(Product, through='OrderItem', related_name='orders')
	notes = models.TextField(blank=True)

	def __str__(self):
		return f"Order {self.id} — {self.supplier.name}"


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.PROTECT)
	quantity = models.IntegerField()
	price = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return f"{self.quantity}×{self.product.name} for Order {self.order.id}"
