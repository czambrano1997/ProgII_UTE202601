from rest_framework import serializers
from .models import Category, Product, Customer, Order, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Category name cannot be empty.")
        if len(value) > 100:
            raise serializers.ValidationError("Category name cannot exceed 100 characters.")
        return value


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value

    def validate_name(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Product name cannot be empty.")
        if len(value) > 200:
            raise serializers.ValidationError("Product name cannot exceed 200 characters.")
        return value


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    def validate_email(self, value):
        if not value or '@' not in value:
            raise serializers.ValidationError("Valid email address is required.")
        return value.lower()

    def validate_first_name(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("First name cannot be empty.")
        return value

    def validate_last_name(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Last name cannot be empty.")
        return value

    def validate_phone(self, value):
        if value and len(value) > 20:
            raise serializers.ValidationError("Phone number cannot exceed 20 characters.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def validate_total(self, value):
        if value < 0:
            raise serializers.ValidationError("Order total cannot be negative.")
        return value

    def validate_status(self, value):
        valid_statuses = ['pending', 'paid', 'shipped', 'cancelled']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Status must be one of {valid_statuses}.")
        return value

    def validate_items(self, value):
        if not isinstance(value, list) or len(value) == 0:
            raise serializers.ValidationError("Items must be a non-empty list.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate_comment(self, value):
        if value and len(value) > 1000:
            raise serializers.ValidationError("Comment cannot exceed 1000 characters.")
        return value
