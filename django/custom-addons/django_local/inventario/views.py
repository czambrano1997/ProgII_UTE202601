from django.shortcuts import render
from .models import Categoria, Producto

# Funciones para vista categoria
def lista_categoria(request):
    categorias = Categoria.objects.all()
    contexto = {
        'carrera': 'PROGRAMACION II',
        'categorias': categorias,
        'total': categorias.count(),
    }
    return render(request, 'inventario/categoria.html', contexto)

# Funciones para vista productos
def lista_productos(request):
    productos = (
        Producto.objects
        .select_related('categoria', 'ficha_tecnica')  # FK y 1:1
        .prefetch_related('proveedores')                # N:M
        .all()
    )
    return render(request, 'inventario/producto.html', {'productos': productos})