from django.contrib import admin

from .models import Categoria, Cliente, Producto


admin.site.register(Categoria)
admin.site.register(Cliente)
admin.site.register(Producto)
