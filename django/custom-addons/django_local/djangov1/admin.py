from django.contrib import admin
from .models import Categoria, Proveedor, Plato, Cliente, Pedido

admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(Plato)
admin.site.register(Cliente)
admin.site.register(Pedido)
