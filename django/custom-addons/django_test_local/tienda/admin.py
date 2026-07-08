from django.contrib import admin

from .models import Categoria, FichaTecnica, Producto, Proveedor

admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(FichaTecnica)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "categoria", "precio", "existencias"]
    filter_horizontal = ["proveedores"]  # widget visual para el M2M
