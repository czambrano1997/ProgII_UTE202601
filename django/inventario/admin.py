from django.contrib import admin

from .models import Proveedor, Categoria, Producto, Cliente, Pedido

admin.site.register(Proveedor)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(Pedido) 
