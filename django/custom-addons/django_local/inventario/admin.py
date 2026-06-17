from django.contrib import admin
from .models import Categoria, Proveedor, FichaTecnica, Producto

# Registro de modelos en apartado administración
admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(FichaTecnica)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'existencias']
    filter_horizontal = ['proveedores']  # widget visual para el M2M