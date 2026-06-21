from django.shortcuts import render
from .models import Cliente, Reserva, Inventario, Gestion_reserva, Paquete, DetalleConsumo


def vista_Home(request):
    context = {
        'total_clientes': Cliente.objects.count(),
        'total_reservas': Reserva.objects.count(),
        'total_paquetes': Paquete.objects.count(),
        'productos_stock': Inventario.objects.count(),
    }
    return render(request, 'djangov1/home.html', context)


def vista_Clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'djangov1/clientes.html', {'clientes': clientes})


def vista_Reservas(request):
    reservas = Reserva.objects.all()
    return render(request, 'djangov1/reservas.html', {'reservas': reservas})


def vista_Inventario(request):
    inventario = Inventario.objects.all()
    return render(request, 'djangov1/inventario.html', {'inventario': inventario})


def vista_Gestion(request):
    gestion_reservas = Gestion_reserva.objects.all()
    return render(request, 'djangov1/gestion_reservas.html', {'gestion_reservas': gestion_reservas})


def vista_paquetes(request):
    paquete = Paquete.objects.all()
    return render(request, 'djangov1/paquete.html', {'paquete': paquete})


def vista_detalle_del_consumo(request):
    consumo = DetalleConsumo.objects.all()
    return render(request, 'djangov1/consumo.html', {'consumo': consumo})