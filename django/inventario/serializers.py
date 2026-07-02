from rest_framework import serializers

from .models import Category, Supplier, Product, InventoryItem, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "created_at"]


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id", "name", "email", "phone", "address", "active"]


class ProductSerializer(serializers.ModelSerializer):
    suppliers = serializers.PrimaryKeyRelatedField(many=True, queryset=Supplier.objects.all(), required=False)

    class Meta:
        model = Product
        fields = ["id", "name", "sku", "description", "price", "category", "suppliers", "active", "created_at"]

    def create(self, validated_data):
        suppliers = validated_data.pop("suppliers", [])
        product = Product.objects.create(**validated_data)
        product.suppliers.set(suppliers)
        return product

    def update(self, instance, validated_data):
        suppliers = validated_data.pop("suppliers", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if suppliers is not None:
            instance.suppliers.set(suppliers)
        return instance


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ["id", "product", "quantity", "location", "last_updated"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "supplier", "date", "total", "notes"]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "quantity", "price"]
