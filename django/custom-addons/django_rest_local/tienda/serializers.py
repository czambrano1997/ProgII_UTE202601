from rest_framework import serializers
from .models import Producto

class ProductoSerializer(
    serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [
            'id',
            'nombre',
            'precio',
            'stock',
        ]

    def validate_precio (self,value):
        if value <= 0:
            raise serializers.ValidationError(
                    'Debe ser > 0')
        return value