from django.contrib import admin
from .models import Autor,Cartegoria,Libro,Usuario,Prestamo
# Register your models here.
admin.site.register(Autor)
admin.site.register(Cartegoria)
admin.site.register(Libro)
admin.site.register(Usuario)
admin.site.register(Prestamo)
