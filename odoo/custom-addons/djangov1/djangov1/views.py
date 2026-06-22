from django.shortcuts import redirect, render

from .forms import ActorForm, ObraForm
from .models import Actor, Boleto, Funcion, Obra, Participacion


def inicio(request):
    return render(request, 'djangov1/index.html')


def lista_obras(request):
    obras = Obra.objects.all()
    return render(request, 'djangov1/lista_obras.html', {'obras': obras})


def crear_obra(request):
    if request.method == 'POST':
        form = ObraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_obras')
    else:
        form = ObraForm()
    return render(request, 'djangov1/crear_obra.html', {'form': form})


def lista_actores(request):
    actores = Actor.objects.all()
    return render(request, 'djangov1/lista_actores.html', {'actores': actores})


def crear_actor(request):
    if request.method == 'POST':
        form = ActorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_actores')
    else:
        form = ActorForm()
    return render(request, 'djangov1/crear_actor.html', {'form': form})


def lista_funciones(request):
    funciones = Funcion.objects.select_related('obra').all()
    return render(request, 'djangov1/lista_funciones.html', {'funciones': funciones})


def lista_participaciones(request):
    participaciones = Participacion.objects.select_related('actor', 'obra').all()
    return render(request, 'djangov1/lista_participaciones.html', {'participaciones': participaciones})


def lista_boletos(request):
    boletos = Boleto.objects.select_related('funcion', 'funcion__obra').all()
    return render(request, 'djangov1/lista_boletos.html', {'boletos': boletos})
