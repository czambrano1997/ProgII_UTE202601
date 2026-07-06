from django.contrib import admin
from .models import Producto, Pedido, DetallePedido

# --- CONFIGURACIÓN PARA DETALLES DEL PEDIDO ---
# Esto permite que cuando abras un Pedido, veas la lista de panes abajo (Inline)
class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    # Al vendedor solo le dejamos ver lo que compraron, no cambiarlo
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ('producto', 'cantidad', 'precio_unitario')
        return ()

# --- CONFIGURACIÓN DE PRODUCTOS (PANES) ---
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock')
    search_fields = ('nombre',)
    list_filter = ('categoria',)

    def get_readonly_fields(self, request, obj=None):
        """
        Si es el Vendedor (Staff), bloqueamos todo menos el STOCK.
        Si eres el Dueño (Superusuario), editas todo.
        """
        if not request.user.is_superuser:
            return ('nombre', 'precio', 'categoria', 'descripcion', 'imagen')
        return ()

    def has_delete_permission(self, request, obj=None):
        """ Solo el Dueño puede borrar productos del sistema """
        if not request.user.is_superuser:
            return False
        return True

# --- CONFIGURACIÓN DE PEDIDOS (VENTAS) ---
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha_pedido', 'total', 'completado')
    list_filter = ('completado', 'fecha_pedido')
    inlines = [DetallePedidoInline] # Aquí se ven los productos del pedido

    def get_readonly_fields(self, request, obj=None):
        """ 
        El vendedor puede ver el pedido y marcarlo como completado, 
        pero no puede cambiar el cliente ni el total.
        """
        if not request.user.is_superuser:
            return ('cliente', 'fecha_pedido', 'total')
        return ()

    def has_delete_permission(self, request, obj=None):
        """ Evita que los vendedores borren registros de ventas """
        if not request.user.is_superuser:
            return False
        return True