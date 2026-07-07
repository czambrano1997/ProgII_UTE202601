from django.contrib import admin
from .models import Categoria, Cliente, DetallePedido, Pedido, Producto

admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(Categoria)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
