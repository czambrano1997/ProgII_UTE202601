from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Producto, Pedido, DetallePedido

try:
    from .models import Categoria
except ImportError:
    Categoria = None


class ProductoSerializer(serializers.ModelSerializer):
    categoria_display = serializers.CharField(source='get_categoria_display', read_only=True)

    class Meta:
        model = Producto
        fields = '__all__'


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'


class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


if Categoria is None:
    class CategoriaSerializer(serializers.Serializer):
        codigo = serializers.CharField(required=False)
        nombre = serializers.CharField(required=False)
else:
    class CategoriaSerializer(serializers.ModelSerializer):
        class Meta:
            model = Categoria
            fields = '__all__'