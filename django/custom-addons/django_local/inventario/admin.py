from django.contrib import admin
from django.contrib import admin
from .models import Proveedor, Categoria, Producto, Cliente, RegistroVenta

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre_empresa', 'email', 'activo')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_venta', 'stock_actual', 'categoria')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cedula')

@admin.register(RegistroVenta)
class RegistroVentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'cliente', 'cantidad', 'total_pago')