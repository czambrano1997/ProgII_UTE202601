from django.contrib import admin
from .models import Autor, Categoria, Libro, Usuario, Prestamo

admin.site.register(Autor)
admin.site.register(Categoria)
admin.site.register(Libro)
admin.site.register(Usuario)
admin.site.register(Prestamo)
