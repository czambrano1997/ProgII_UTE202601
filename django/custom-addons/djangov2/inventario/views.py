from django.db.models import Count, Sum
from django.shortcuts import render

from .models import Categoria, Cliente, DetallePedido, Pedido, Producto


def inicio(request):
    """Pagina principal tipo tienda."""
    productos = Producto.objects.select_related('categoria').filter(activo=True)[:8]
    categorias = Categoria.objects.filter(activo=True).annotate(total_productos=Count('productos'))[:6]
    pedidos_recientes = Pedido.objects.select_related('cliente').prefetch_related('detalles')[:5]

    total_vendido = Pedido.objects.aggregate(total=Sum('total'))['total'] or 0
    estadisticas = {
        'productos': Producto.objects.count(),
        'categorias': Categoria.objects.count(),
        'clientes': Cliente.objects.count(),
        'pedidos': Pedido.objects.count(),
        'ventas': total_vendido,
    }

    return render(request, 'inventario/inicio.html', {
        'productos': productos,
        'categorias': categorias,
        'pedidos_recientes': pedidos_recientes,
        'estadisticas': estadisticas,
    })


def tienda(request):
    """Catalogo visual de productos con filtro simple."""
    categoria_id = request.GET.get('categoria')
    buscar = request.GET.get('buscar', '').strip()

    productos = Producto.objects.select_related('categoria').filter(activo=True)

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    if buscar:
        productos = productos.filter(nombre__icontains=buscar)

    categorias = Categoria.objects.filter(activo=True)

    return render(request, 'inventario/tienda.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_id': categoria_id,
        'buscar': buscar,
    })


def panel_categorias(request):
    categorias = Categoria.objects.annotate(total_productos=Count('productos'))
    return render(request, 'inventario/categorias.html', {'categorias': categorias})


def panel_clientes(request):
    clientes = Cliente.objects.annotate(total_pedidos=Count('pedidos'))
    return render(request, 'inventario/clientes.html', {'clientes': clientes})


def panel_pedidos(request):
    pedidos = Pedido.objects.select_related('cliente').prefetch_related('detalles__producto')
    return render(request, 'inventario/pedidos.html', {'pedidos': pedidos})
