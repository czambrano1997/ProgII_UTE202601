from rest_framework import serializers
from .models import Categoria,Proveedor, FichaTecnica, Producto, Cliente, Pedido, DetallePedido, Bodega, Descuento

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Categoria
        fields = [
            'id',
            'nombre',
            'descripcion',
            'precio',
            'active',
            'create_date',
        ]
    
    def validate_active(self,value):
        if not value:
            raise serializers.ValidationError('Debe estar activa')
        return value
    
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Proveedor
        fields = [
            'id',
            'nombre',
            'contacto',
            'pais',
        ]
    
    def validate_precio(self,value):
        if value <=0:
            raise serializers.ValidationError('Debe ser >0')
        return value
    
class FichaTecSerializer(serializers.ModelSerializer):
    class Meta: 
        model = FichaTecnica
        fields = [
            'id',
            'nombre',
            'precio',
            'stock',
        ]
    
    def validate_precio(self,value):
        if value <=0:
            raise serializers.ValidationError('Debe ser >0')
        return value    

class ProductoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Producto
        fields = [
            'id',
            'nombre',
            'precio',
            'stock',
        ]
    
    def validate_precio(self,value):
        if value <=0:
            raise serializers.ValidationError('Debe ser >0')
        return value
    
class ClienteSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Cliente
        fields = [
            'nombre',
            'email',
            'phone_number',
            'city',
            'active',
            'create_date',
        ]
    
    def validate_precio(self,value):
        if value <=0:
            raise serializers.ValidationError('Debe ser >0')
        return value

class PedidoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Pedido
        fields = [
            'status',
            'id_cliente',
            'date',
            'status',
            'total',
            'notes',
        ]
    
    def validate_precio(self,value):
        if value <=0:
            raise serializers.ValidationError('Debe ser >0')
        return value

class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = DetallePedido
        fields = [
            'id_pedido',
            'nombre_producto',
            'stock',
            'unite_price',
        ]
    
    def validate_precio(self,value):
        if value <=0:
            raise serializers.ValidationError('Debe ser >0')
        return value
    
class BodegaSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Bodega
        fields = [
            'localitation',
            'capacity',
            'active',
            'create_date',
        ]
    
    def validate_precio(self,value):
        if value <=0:
            raise serializers.ValidationError('Debe ser >0')
        return value

class DescuentoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Descuento
        fields = [
            'id_producto',
            'porcentaje',
            'date_start',
            'date_end',
            'active',
        ]
    
    def validate_precio(self,value):
        if value <=0:
            raise serializers.ValidationError('Debe ser >0')
        return value