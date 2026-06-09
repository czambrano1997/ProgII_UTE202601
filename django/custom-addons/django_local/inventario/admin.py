from django.contrib import admin
from .models import Categoria

# Register your models here.
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'descripcion']
    list_filter = ['codigo'] 
    search_fields = ['codigo', 'nombre']