from django.contrib import admin
from .models import Categoria, Proveedor, FichaTecnica, Producto, Cliente, Pedido, DetallePedido, Bodega, Descuento

# Registro de modelos en apartado administración
admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(FichaTecnica)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'existencias']
    filter_horizontal = ['proveedores']  # widget visual para el M2M

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'ciudad', 'activo']
    list_filter = ['activo', 'ciudad']
    search_fields = ['nombre', 'email']
 
 
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'estado', 'total', 'fecha']
    list_filter = ['estado']
    search_fields = ['cliente__nombre']
 
 
@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'producto', 'cantidad', 'precio_unitario']
 
 
@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ubicacion', 'capacidad', 'activa']
    list_filter = ['activa']
 
 
@admin.register(Descuento)
class DescuentoAdmin(admin.ModelAdmin):
    list_display = ['producto', 'porcentaje', 'fecha_inicio', 'fecha_fin', 'activo']
    list_filter = ['activo']