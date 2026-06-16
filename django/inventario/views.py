from django.shortcuts import render
from .models import Categoria

# Create your views here.
def lista_categoria(request):
    categorias = Categoria.objects.all()
    return render(request, 'inventario/categoria.html', {'categorias': categorias})