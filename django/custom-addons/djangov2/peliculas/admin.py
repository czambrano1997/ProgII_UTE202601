from django.contrib import admin
from .models import Pelicula, Sala, Funcion, Cliente, Boleto

admin.site.register(Pelicula)
admin.site.register(Sala)
admin.site.register(Funcion)
admin.site.register(Cliente)
admin.site.register(Boleto)
