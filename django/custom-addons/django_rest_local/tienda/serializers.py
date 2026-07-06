from rest_framework import serializers

from .models import Categoria, Producto


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nombre", "descripcion"]


class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)

    class Meta:
        model = Producto
        fields = ["id", "nombre", "precio", "stock", "categoria"]

    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser > 0")
        return value