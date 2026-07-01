from rest_framework import serializers
from .models import TipoFlor, Proveedor, Flor, Cliente, Pedido


class TipoFlorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoFlor
        fields = '__all__'


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'


class FlorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flor
        fields = '__all__'


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

