from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Categoria, Plataforma, Videojuego, Cliente, Venta

admin.site.register(Categoria)
admin.site.register(Plataforma)
admin.site.register(Videojuego)
admin.site.register(Cliente)
admin.site.register(Venta)