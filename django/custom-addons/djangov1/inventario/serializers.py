from rest_framework import serializers
from .models import (
    Categoria, Proveedor, FichaTecnica, Producto,
    Cliente, Pedido, DetallePedido, Bodega, Descuento
)
 
 
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = [
            "id",
            "nombre",
            "codigo",
            "descripcion",
            "activa",
            "creada_en",
        ]
 
 
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = [
            "id",
            "nombre",
            "contacto",
            "pais",
        ]
 
 
class FichaTecnicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FichaTecnica
        fields = [
            "id",
            "producto",
            "peso_kg",
            "dimensiones",
            "garantia_meses",
        ]
 
    def validate_peso_kg(self, value):
        if value <= 0:
            raise serializers.ValidationError("El peso debe ser mayor a 0")
        return value
 
 
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [
            "id",
            "nombre",
            "precio",
            "existencias",
            "categoria",
        ]
 
    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser > 0")
        return value
 
    def validate_existencias(self, value):
        if value < 0:
            raise serializers.ValidationError("Las existencias no pueden ser negativas")
        return value
 
 
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            "id",
            "nombre",
            "email",
            "telefono",
            "ciudad",
            "activo",
            "creado_en",
        ]
 
 
class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = [
            "id",
            "cliente",
            "fecha",
            "estado",
            "total",
            "notas",
        ]
 
    def validate_total(self, value):
        if value < 0:
            raise serializers.ValidationError("El total no puede ser negativo")
        return value
 
 
class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = [
            "id",
            "pedido",
            "producto",
            "cantidad",
            "precio_unitario",
        ]
 
    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser > 0")
        return value
 
 
class BodegaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bodega
        fields = [
            "id",
            "nombre",
            "ubicacion",
            "capacidad",
            "activa",
            "creada_en",
        ]
 
    def validate_capacidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("La capacidad debe ser > 0")
        return value
 
 
class DescuentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Descuento
        fields = [
            "id",
            "producto",
            "porcentaje",
            "fecha_inicio",
            "fecha_fin",
            "activo",
        ]
 
    def validate_porcentaje(self, value):
        if value <= 0 or value > 100:
            raise serializers.ValidationError("El porcentaje debe estar entre 0 y 100")
        return value
 
    def validate(self, data):
        inicio = data.get("fecha_inicio")
        fin = data.get("fecha_fin")
        if inicio and fin and fin < inicio:
            raise serializers.ValidationError(
                "La fecha_fin no puede ser anterior a fecha_inicio"
            )
        return data