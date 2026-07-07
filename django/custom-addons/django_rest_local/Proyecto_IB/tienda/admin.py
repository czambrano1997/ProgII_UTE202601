from django.contrib import admin
from .models import Autor, Editorial, Categoria, Libro, Prestamo

# Register your models here.
admin.site.register(Autor)
admin.site.register(Editorial)
admin.site.register(Categoria)
admin.site.register(Libro)
admin.site.register(Prestamo)
