from rest_framework import serializers
from .models import Categoria, Proveedor, Plato, Cliente, Pedido


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = [
            'id',
            'nombre',
            'descripcion',
            'disponible'
        ]


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = [
            'id',
            'nombre',
            'telefono',
            'correo'
        ]


class PlatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plato
        fields = [
            'id',
            'nombre',
            'descripcion',
            'precio',
            'disponible',
            'categoria',
            'proveedor'
        ]


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            'id',
            'nombre',
            'telefono',
            'correo'
        ]


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = [
            'id',
            'cliente',
            'plato',
            'cantidad',
            'fecha'
        ]