from django.contrib import admin

from .models import Autor, Editorial, Categoria, Libro, Prestamo


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'activo')
    search_fields = ('nombre', 'apellido', 'email')
    list_filter = ('activo',)


@admin.register(Editorial)
class EditorialAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'activo')
    search_fields = ('nombre', 'email')
    list_filter = ('activo',)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'editorial', 'categoria', 'disponible', 'precio')
    search_fields = ('titulo', 'isbn', 'autor__nombre', 'editorial__nombre')
    list_filter = ('disponible', 'editorial', 'categoria')


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('libro', 'usuario_nombre', 'fecha_prestamo', 'fecha_devolucion', 'devuelto')
    search_fields = ('libro__titulo', 'usuario_nombre', 'usuario_email')
    list_filter = ('devuelto',)
