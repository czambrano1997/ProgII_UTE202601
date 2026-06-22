from django.contrib import admin

from .models import Actor, Boleto, Funcion, Obra, Participacion


@admin.register(Obra)
class ObraAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'duracion_min', 'fecha_estreno')
    search_fields = ('titulo',)
    list_filter = ('fecha_estreno',)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'edad', 'nacionalidad', 'email')
    search_fields = ('nombre', 'nacionalidad')
    list_filter = ('nacionalidad',)


@admin.register(Funcion)
class FuncionAdmin(admin.ModelAdmin):
    list_display = ('obra', 'fecha', 'sala', 'entradas_disponibles')
    search_fields = ('obra__titulo', 'sala')
    list_filter = ('sala',)


@admin.register(Participacion)
class ParticipacionAdmin(admin.ModelAdmin):
    list_display = ('actor', 'obra', 'personaje')
    search_fields = ('actor__nombre', 'obra__titulo', 'personaje')
    list_filter = ('obra',)


@admin.register(Boleto)
class BoletoAdmin(admin.ModelAdmin):
    list_display = ('funcion', 'cliente_nombre', 'cliente_email', 'asiento', 'precio', 'confirmado')
    search_fields = ('cliente_nombre', 'cliente_email', 'funcion__obra__titulo')
    list_filter = ('confirmado',)
