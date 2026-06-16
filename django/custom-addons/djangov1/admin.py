from django.contrib import admin
from .models import Autor, CategoriaLibro, Libro, Cliente, Prestamo


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'activo', 'created_at')
    search_fields = ('nombre', 'email')
    list_filter = ('activo',)


@admin.register(CategoriaLibro)
class CategoriaLibroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'activo')
    search_fields = ('nombre', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'isbn', 'categoria', 'precio', 'disponible', 'fecha_publicacion')
    search_fields = ('titulo', 'isbn', 'categoria__nombre')
    list_filter = ('categoria', 'disponible')
    filter_horizontal = ('autores',)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'activo', 'fecha_registro')
    search_fields = ('nombre', 'email', 'telefono')
    list_filter = ('activo',)


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'libro', 'fecha_prestamo', 'fecha_devolucion', 'devuelto', 'multa')
    search_fields = ('cliente__nombre', 'libro__titulo')
    list_filter = ('devuelto',)
