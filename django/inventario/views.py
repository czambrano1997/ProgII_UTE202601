from django.shortcuts import render
from .models import Categoria

# Create your views here.
def lista_categorias(request):
    categorias = Categoria.objects.all().order_by('nombre')
    return render(request, 'inventario/categoria.html', {'categorias': categorias})
