from django.db import models


class Category(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.name


class Product(models.Model):
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	stock = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class Customer(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField(unique=True)
	phone = models.CharField(max_length=20, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.first_name} {self.last_name}"


class Order(models.Model):
	STATUS_CHOICES = [
		('pending', 'Pending'),
		('paid', 'Paid'),
		('shipped', 'Shipped'),
		('cancelled', 'Cancelled'),
	]

	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
	items = models.JSONField(help_text='List of order items (product_id, quantity, price)')
	total = models.DecimalField(max_digits=12, decimal_places=2)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Order #{self.id} - {self.customer}"


class Review(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	rating = models.PositiveSmallIntegerField()
	comment = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Review {self.id} - {self.product} ({self.rating})"
