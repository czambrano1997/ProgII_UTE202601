from django.contrib import admin

from .forms import DetallePedidoAdminForm
from .models import (
    Categoria,
    Cliente,
    DetallePedido,
    Pedido,
    Producto,
    Proveedor,
)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "activa",
        "creada_en",
    )

    list_filter = (
        "activa",
    )

    search_fields = (
        "nombre",
        "descripcion",
    )

    prepopulated_fields = {
        "slug": ("nombre",),
    }


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "correo",
        "telefono",
        "activo",
        "fecha_registro",
    )

    list_filter = (
        "activo",
    )

    search_fields = (
        "nombre",
        "correo",
        "telefono",
    )


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "sku",
        "categoria",
        "proveedor",
        "precio",
        "stock",
        "stock_minimo",
        "mostrar_reposicion",
        "disponible",
    )

    list_filter = (
        "disponible",
        "categoria",
        "proveedor",
    )

    search_fields = (
        "nombre",
        "sku",
        "descripcion",
    )

    list_select_related = (
        "categoria",
        "proveedor",
    )

    prepopulated_fields = {
        "slug": ("nombre",),
    }

    @admin.display(
        description="Stock bajo",
        boolean=True,
    )
    def mostrar_reposicion(self, obj):
        return obj.necesita_reposicion


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        "nombre_completo",
        "correo",
        "telefono",
        "fecha_nacimiento",
        "mostrar_edad",
        "activo",
    )

    list_filter = (
        "activo",
    )

    search_fields = (
        "nombres",
        "apellidos",
        "correo",
        "telefono",
    )

    readonly_fields = (
        "mostrar_edad",
        "creado_en",
    )

    fields = (
        "nombres",
        "apellidos",
        "correo",
        "telefono",
        "direccion",
        "fecha_nacimiento",
        "mostrar_edad",
        "activo",
        "creado_en",
    )

    @admin.display(description="Edad")
    def mostrar_edad(self, obj):
        if not obj or obj.edad is None:
            return "Se calculará al guardar"

        return f"{obj.edad} años"


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    form = DetallePedidoAdminForm
    extra = 1

    autocomplete_fields = (
        "producto",
    )

    fields = (
        "producto",
        "cantidad",
        "precio_unitario",
        "descuento",
        "mostrar_subtotal",
    )

    readonly_fields = (
        "mostrar_subtotal",
    )

    @admin.display(description="Subtotal")
    def mostrar_subtotal(self, obj):
        if not obj or not obj.pk:
            return "Se calculará al guardar"

        return f"${obj.subtotal:.2f}"



@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "cliente",
        "fecha",
        "estado",
        "entregado",
        "mostrar_cantidad_productos",
        "mostrar_total",
    )

    list_filter = (
        "estado",
        "entregado",
        "fecha",
    )

    search_fields = (
        "codigo",
        "cliente__nombres",
        "cliente__apellidos",
        "cliente__correo",
    )

    list_select_related = (
        "cliente",
    )

    readonly_fields = (
        "mostrar_total",
    )

    inlines = (
        DetallePedidoInline,
    )

    @admin.display(description="Productos")
    def mostrar_cantidad_productos(self, obj):
        return obj.detalles.count()

    @admin.display(description="Total")
    def mostrar_total(self, obj):
        if not obj or not obj.pk:
            return "Se calculará al guardar"

        return f"${obj.total:.2f}"


@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    form = DetallePedidoAdminForm

    list_display = (
        "pedido",
        "producto",
        "cantidad",
        "precio_unitario",
        "descuento",
        "mostrar_bruto",
        "mostrar_descuento",
        "mostrar_subtotal",
    )

    list_select_related = (
        "pedido",
        "producto",
    )

    search_fields = (
        "pedido__codigo",
        "producto__nombre",
        "producto__sku",
    )

    autocomplete_fields = (
        "pedido",
        "producto",
    )

    @admin.display(description="Subtotal bruto")
    def mostrar_bruto(self, obj):
        return f"${obj.subtotal_sin_descuento:.2f}"

    @admin.display(description="Valor descontado")
    def mostrar_descuento(self, obj):
        return f"${obj.valor_descuento:.2f}"

    @admin.display(description="Subtotal final")
    def mostrar_subtotal(self, obj):
        return f"${obj.subtotal:.2f}"
