from django.contrib import admin
from .models import Cliente,Reserva,Paquete,Inventario,Gestion_reserva,DetalleConsumo

# Register your models here.

admin.site.register(Cliente)
admin.site.register(Reserva)
admin.site.register(Paquete)
admin.site.register(Inventario)
admin.site.register(Gestion_reserva)
admin.site.register(DetalleConsumo)