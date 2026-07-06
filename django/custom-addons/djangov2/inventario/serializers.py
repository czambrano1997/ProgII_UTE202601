from rest_framework import serializers
from .models import Categoria, Cliente, DetallePedido, Pedido, Producto


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)

    class Meta:
        model = Producto
        fields = [
            'id', 'categoria', 'categoria_nombre', 'nombre', 'descripcion',
            'precio', 'stock', 'activo'
        ]


class ClienteSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = Cliente
        fields = [
            'id', 'nombres', 'apellidos', 'nombre_completo',
            'cedula', 'correo', 'telefono'
        ]

    def get_nombre_completo(self, obj):
        return f'{obj.nombres} {obj.apellidos}'


class DetallePedidoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)

    class Meta:
        model = DetallePedido
        fields = [
            'id', 'pedido', 'producto', 'producto_nombre',
            'cantidad', 'precio_unitario', 'subtotal'
        ]
        read_only_fields = ['subtotal']


class PedidoSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.__str__', read_only=True)
    detalles = DetallePedidoSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = [
            'id', 'cliente', 'cliente_nombre', 'fecha',
            'estado', 'total', 'detalles'
        ]
        read_only_fields = ['fecha', 'total']
