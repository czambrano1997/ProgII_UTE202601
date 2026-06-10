from django.shortcuts import render
from django.http import JsonResponse
from .models import Categoria, Producto
from django.db.models import Sum, F, DecimalField, ExpressionWrapper


def categorias_list(request):
	"""Devuelve la lista de categorias como JSON."""
	categorias = list(Categoria.objects.values("id", "nombre", "descripcion", "creado"))
	return JsonResponse(categorias, safe=False)


def categorias_page(request):
	"""Renderiza el template con la lista de categorías."""
	categorias = Categoria.objects.all()
	return render(request, "inventario/categoria.html", {"categorias": categorias})


def panel_inventario(request):
	"""Panel simple que muestra estadísticas y listado de productos."""
	productos = Producto.objects.all()
	categorias = Categoria.objects.all()
	total_productos = productos.count()
	total_categorias = categorias.count()
	total_valor = (
		productos.aggregate(
			total=Sum(
				ExpressionWrapper(F('precio') * F('existencia'), output_field=DecimalField())
			)
		)['total'] or 0
	)
	return render(
		request,
		"inventario/panel.html",
		{
			"productos": productos,
			"categorias": categorias,
			"total_productos": total_productos,
			"total_categorias": total_categorias,
			"total_valor": total_valor,
		},
	)
