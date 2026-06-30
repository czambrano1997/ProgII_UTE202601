from rest_framework import serializers
from .models import (
    Categoria,
    Proveedor,
    Producto,
    Cliente,
    Venta,
    DetalleVenta,
)


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'activa', 'descripcion']


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = [
            'id', 'empresa', 'email_contacto',
            'sitio_web', 'fecha_asociacion'
        ]


class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(
        source='categoria.nombre',
        read_only=True
    )
    proveedor_empresa = serializers.CharField(
        source='proveedor.empresa',
        read_only=True
    )

    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'precio', 'stock',
            'categoria', 'categoria_nombre',
            'proveedor', 'proveedor_empresa',
            'fecha_ingreso'
        ]

    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'El precio debe ser mayor a 0.'
            )
        return value


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            'id', 'identificacion', 'nombre_completo',
            'fecha_nacimiento', 'es_vip'
        ]


class DetalleVentaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(
        source='producto.nombre',
        read_only=True
    )
    subtotal = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = DetalleVenta
        fields = [
            'id', 'venta', 'producto', 'producto_nombre',
            'cantidad', 'precio_unitario', 'subtotal'
        ]


class VentaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(
        source='cliente.nombre_completo',
        read_only=True
    )
    detalles = DetalleVentaSerializer(many=True, read_only=True)

    class Meta:
        model = Venta
        fields = [
            'id', 'cliente', 'cliente_nombre',
            'fecha_venta', 'total', 'observaciones',
            'detalles'
        ]