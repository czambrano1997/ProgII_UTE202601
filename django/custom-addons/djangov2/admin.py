from django.contrib import admin

from .models import Categoria, Cliente, DetallePedido, Pedido, Producto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "activo", "creado_en")
    search_fields = ("nombre", "descripcion")
    list_filter = ("activo",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "categoria", "precio", "stock", "activo")
    search_fields = ("nombre", "descripcion", "categoria__nombre")
    list_filter = ("activo", "categoria")


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("id", "cedula", "nombres", "apellidos", "email", "activo")
    search_fields = ("cedula", "nombres", "apellidos", "email")
    list_filter = ("activo",)


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "estado", "fecha", "total")
    search_fields = ("cliente__nombres", "cliente__apellidos", "estado")
    list_filter = ("estado", "activo")
    inlines = [DetallePedidoInline]


@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "pedido", "producto", "cantidad", "precio_unitario", "subtotal")
    search_fields = ("producto__nombre", "pedido__cliente__nombres", "pedido__cliente__apellidos")
