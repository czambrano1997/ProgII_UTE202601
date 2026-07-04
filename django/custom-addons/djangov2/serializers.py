from rest_framework import serializers
from .models import Cliente, Reserva, Paquete, Inventario, Canchas


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'


class PaqueteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paquete
        fields = '__all__'


class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields = '__all__'


class CanchasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canchas
        fields = '__all__'
