from django.shortcuts import render
from .models import Categoria, Producto

# Funciones para vista categoria
def lista_categoria(request):
    categorias = {Categoria.objects.all()} 
    return render(request, 'inventario/categoria.html', {'categorias': categorias})
