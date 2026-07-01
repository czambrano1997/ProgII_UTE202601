from rest_framework import serializers

from .models import Categoria, Cliente, DetallePedido, Pedido, Producto


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = [
            "id",
            "nombre",
            "descripcion",
            "activo",
            "creado_en",
            "actualizado_en",
        ]
        read_only_fields = ["id", "creado_en", "actualizado_en"]


class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source="categoria.nombre", read_only=True)

    class Meta:
        model = Producto
        fields = [
            "id",
            "categoria",
            "categoria_nombre",
            "nombre",
            "descripcion",
            "precio",
            "stock",
            "activo",
            "creado_en",
            "actualizado_en",
        ]
        read_only_fields = ["id", "categoria_nombre", "creado_en", "actualizado_en"]

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo.")
        return value


class ClienteSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = Cliente
        fields = [
            "id",
            "cedula",
            "nombres",
            "apellidos",
            "nombre_completo",
            "email",
            "telefono",
            "direccion",
            "activo",
            "creado_en",
            "actualizado_en",
        ]
        read_only_fields = ["id", "nombre_completo", "creado_en", "actualizado_en"]

    def get_nombre_completo(self, obj):
        return f"{obj.nombres} {obj.apellidos}"

    def validate_cedula(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("La cédula/RUC debe contener solo números.")
        if len(value) not in (10, 13):
            raise serializers.ValidationError("La cédula debe tener 10 dígitos o el RUC 13 dígitos.")
        return value


class DetallePedidoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source="producto.nombre", read_only=True)
    precio_unitario = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = DetallePedido
        fields = [
            "id",
            "pedido",
            "producto",
            "producto_nombre",
            "cantidad",
            "precio_unitario",
            "subtotal",
        ]
        read_only_fields = [
            "id",
            "producto_nombre",
            "precio_unitario",
            "subtotal",
        ]

    def validate(self, attrs):
        producto = attrs.get("producto") or getattr(self.instance, "producto", None)
        cantidad = attrs.get("cantidad") or getattr(self.instance, "cantidad", None)

        if producto is not None and cantidad is not None and cantidad > producto.stock:
            raise serializers.ValidationError(
                {"cantidad": "La cantidad no puede superar el stock disponible."}
            )

        return attrs

    def create(self, validated_data):
        producto = validated_data["producto"]
        validated_data["precio_unitario"] = producto.precio
        return super().create(validated_data)

    def update(self, instance, validated_data):
        producto = validated_data.get("producto", instance.producto)

        if "producto" in validated_data:
            validated_data["precio_unitario"] = producto.precio

        return super().update(instance, validated_data)

class PedidoSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source="cliente.__str__", read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    detalles = DetallePedidoSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = [
            "id",
            "cliente",
            "cliente_nombre",
            "fecha",
            "estado",
            "observacion",
            "activo",
            "total",
            "detalles",
            "actualizado_en",
        ]
        read_only_fields = ["id", "cliente_nombre", "fecha", "total", "detalles", "actualizado_en"]
