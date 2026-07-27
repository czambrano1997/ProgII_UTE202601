from django.shortcuts import render, redirect
from .services import OdooAPIService

# --- CARRERAS ---
def lista_carreras(request):
    carreras = OdooAPIService.get_all('ou.carrera')
    return render(request, 'cliente_ute/carreras.html', {'carreras': carreras})

def crear_carrera(request):
    if request.method == 'POST':
        payload = {'name': request.POST.get('name'), 'code': request.POST.get('code')}
        OdooAPIService.create('ou.carrera', payload)
    return redirect('lista_carreras')

def eliminar_carrera(request, carrera_id):
    OdooAPIService.delete('ou.carrera', carrera_id)
    return redirect('lista_carreras')


# --- PERIODOS ---
def lista_periodos(request):
    periodos = OdooAPIService.get_all('ou.periodo')
    return render(request, 'cliente_ute/periodos.html', {'periodos': periodos})

def crear_periodo(request):
    if request.method == 'POST':
        payload = {'name': request.POST.get('name')}
        OdooAPIService.create('ou.periodo', payload)
    return redirect('lista_periodos')

def eliminar_periodo(request, periodo_id):
    OdooAPIService.delete('ou.periodo', periodo_id)
    return redirect('lista_periodos')


# --- AULAS ---
def lista_aulas(request):
    aulas = OdooAPIService.get_all('ou.aula')
    return render(request, 'cliente_ute/aulas.html', {'aulas': aulas})

def crear_aula(request):
    if request.method == 'POST':
        payload = {'name': request.POST.get('name')}
        OdooAPIService.create('ou.aula', payload)
    return redirect('lista_aulas')

def eliminar_aula(request, aula_id):
    OdooAPIService.delete('ou.aula', aula_id)
    return redirect('lista_aulas')


# --- MATERIAS ---
def lista_materias(request):
    materias = OdooAPIService.get_all('ou.signature')
    return render(request, 'cliente_ute/materias.html', {'materias': materias})

def crear_materia(request):
    if request.method == 'POST':
        payload = {'name': request.POST.get('name')}
        OdooAPIService.create('ou.signature', payload)
    return redirect('lista_materias')

def eliminar_materia(request, materia_id):
    OdooAPIService.delete('ou.signature', materia_id)
    return redirect('lista_materias')


# --- USUARIOS ---
def lista_usuarios(request):
    usuarios = OdooAPIService.get_all('sistema.usuarios')
    return render(request, 'cliente_ute/usuarios.html', {'usuarios': usuarios})

def crear_usuario(request):
    if request.method == 'POST':
        payload = {'name': request.POST.get('name'), 'email': request.POST.get('email')}
        OdooAPIService.create('sistema.usuarios', payload)
    return redirect('lista_usuarios')

def eliminar_usuario(request, usuario_id):
    OdooAPIService.delete('sistema.usuarios', usuario_id)
    return redirect('lista_usuarios')