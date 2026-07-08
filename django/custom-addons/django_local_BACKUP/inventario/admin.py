from django.contrib import admin
from .models import Categoria, Proveedor, FichaTecnica, Producto
from .models import Cliente, Pedido, DetallePedido, Bodega, Descuento

# Registro de modelos en apartado administración
admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(FichaTecnica)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'existencias']
    filter_horizontal = ['proveedores']  # widget visual para el M2M

# Modelos nuevos
admin.site.register(Cliente)
admin.site.register(Bodega)
admin.site.register(Descuento)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'estado', 'total', 'fecha']

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'producto', 'cantidad', 'precio_unitario']