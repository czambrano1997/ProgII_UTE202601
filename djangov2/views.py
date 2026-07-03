from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Category, Product, Customer, Order, Review
from .serializers import (
	CategorySerializer,
	ProductSerializer,
	CustomerSerializer,
	OrderSerializer,
	ReviewSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	permission_classes = [AllowAny]


class ProductViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	permission_classes = [AllowAny]


class CustomerViewSet(viewsets.ModelViewSet):
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer
	permission_classes = [AllowAny]


class OrderViewSet(viewsets.ModelViewSet):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer
	permission_classes = [AllowAny]


class ReviewViewSet(viewsets.ModelViewSet):
	queryset = Review.objects.all()
	serializer_class = ReviewSerializer
	permission_classes = [AllowAny]
