from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .forms import ProductoForm
from .models import Categoria, Producto
from .serializers import CategoriaSerializer, ProductoSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


def home_view(request):
    categorias = Categoria.objects.all().order_by("nombre")
    return render(request, "tienda/home.html", {"categorias": categorias})


def producto_list(request):
    productos = Producto.objects.all().order_by("nombre")
    return render(request, "tienda/producto_list.html", {"productos": productos})


def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, "tienda/producto_detail.html", {"producto": producto})


def producto_create(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            return redirect("producto_detail", pk=producto.pk)
    else:
        form = ProductoForm()

    return render(request, "tienda/producto_form.html", {"form": form, "title": "Crear producto"})


def categoria_list(request):
    categorias = Categoria.objects.all().order_by("nombre")
    return render(request, "tienda/categoria_list.html", {"categorias": categorias})


def categoria_detail(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    return render(request, "tienda/categoria_detail.html", {"categoria": categoria})