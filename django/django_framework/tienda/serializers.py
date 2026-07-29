from rest_framework import serializers

from .models import Categoria, Cliente, Producto


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nombre", "descripcion"]


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ["id", "nombre", "email", "telefono"]


class ProductoSerializer(serializers.ModelSerializer):
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Producto
        fields = ["id", "nombre", "precio", "stock", "categoria"]
