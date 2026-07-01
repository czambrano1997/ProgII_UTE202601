from django.shortcuts import render

from .models import Categoria, Producto


def lista_categoria(request):
    categorias = Categoria.objects.all()
    contexto = {
        "carrera": "PROGRAMACION II",
        "categorias": categorias,
        "total": categorias.count(),
    }
    return render(request, "tienda/categoria.html", contexto)


def lista_productos(request):
    productos = (
        Producto.objects
        .select_related("categoria", "ficha_tecnica")  # FK y 1:1
        .prefetch_related("proveedores")                # N:M
        .all()
    )
    contexto = {
        "productos": productos,
        "total": productos.count(),
    }
    return render(request, "tienda/producto.html", contexto)
