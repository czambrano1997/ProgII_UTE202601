from django.contrib import admin
from .models import TipoFlor, Proveedor, Flor, Cliente, Pedido

admin.site.register(TipoFlor)
admin.site.register(Proveedor)
admin.site.register(Flor)
admin.site.register(Cliente)
admin.site.register(Pedido)