from django.contrib import admin
from .models import Categoria, Proveedor, Producto, Cliente, Venta

# Registro simple para cumplir el requerimiento
admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(Venta)