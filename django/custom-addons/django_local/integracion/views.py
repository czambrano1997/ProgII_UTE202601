"""Vistas de la app integracion.

Cada modelo tiene 3 vistas:
  - lista:   GET  → muestra tabla HTML con registros de Odoo
  - crear:   GET/POST → formulario que envía POST a Odoo
  - eliminar: GET/POST → confirmación y DELETE a Odoo
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from . import odoo_client


# ============================================================
# UTILIDAD: filtro de template para acceder a dict por clave
# ============================================================
from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    """Permite acceder a valores de diccionario en templates: {{ reg|get_item:'name' }}"""
    if dictionary is None:
        return None
    return dictionary.get(key)


# ============================================================
# MODELO: CARRERA
# ============================================================

def carrera_lista(request):
    resultado = odoo_client.obtener_todos('carrera')
    registros = resultado.get('data', []) if resultado.get('status') == 'success' else []
    if resultado.get('status') == 'error':
        messages.error(request, resultado.get('message'))
    return render(request, 'integracion/lista.html', {
        'titulo': 'Carreras',
        'modelo': 'carrera',
        'registros': registros,
        'campos': ['id', 'name', 'codigo', 'modalidad']
    })


def carrera_crear(request):
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'codigo': request.POST.get('codigo'),
            'modalidad': request.POST.get('modalidad')
        }
        resultado = odoo_client.crear_registro('carrera', data)
        if resultado.get('status') == 'success':
            messages.success(request, 'Carrera creada exitosamente')
            return redirect('integracion:carrera_lista')
        else:
            messages.error(request, resultado.get('message'))
    return render(request, 'integracion/form_crear.html', {
        'titulo': 'Nueva Carrera',
        'modelo': 'carrera',
        'campos': [
            {'name': 'name', 'label': 'Nombre', 'tipo': 'text'},
            {'name': 'codigo', 'label': 'Código', 'tipo': 'text'},
            {'name': 'modalidad', 'label': 'Modalidad', 'tipo': 'select',
             'opciones': [('presencial', 'Presencial'), ('virtual', 'Virtual'), ('hibrida', 'Híbrida')]}
        ]
    })


def carrera_eliminar(request, pk):
    if request.method == 'POST':
        resultado = odoo_client.eliminar_registro('carrera', pk)
        if resultado.get('status') == 'success':
            messages.success(request, 'Carrera eliminada')
        else:
            messages.error(request, resultado.get('message'))
        return redirect('integracion:carrera_lista')
    return render(request, 'integracion/confirmar_eliminar.html', {
        'titulo': 'Eliminar Carrera',
        'modelo': 'carrera',
        'id': pk
    })


# ============================================================
# MODELO: PERIODO
# ============================================================

def periodo_lista(request):
    resultado = odoo_client.obtener_todos('periodo')
    registros = resultado.get('data', []) if resultado.get('status') == 'success' else []
    if resultado.get('status') == 'error':
        messages.error(request, resultado.get('message'))
    return render(request, 'integracion/lista.html', {
        'titulo': 'Períodos Académicos',
        'modelo': 'periodo',
        'registros': registros,
        'campos': ['id', 'name', 'fecha_inicio', 'fecha_fin', 'activo']
    })


def periodo_crear(request):
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'fecha_inicio': request.POST.get('fecha_inicio'),
            'fecha_fin': request.POST.get('fecha_fin'),
            'activo': request.POST.get('activo') == 'on'
        }
        resultado = odoo_client.crear_registro('periodo', data)
        if resultado.get('status') == 'success':
            messages.success(request, 'Período creado exitosamente')
            return redirect('integracion:periodo_lista')
        else:
            messages.error(request, resultado.get('message'))
    return render(request, 'integracion/form_crear.html', {
        'titulo': 'Nuevo Período Académico',
        'modelo': 'periodo',
        'campos': [
            {'name': 'name', 'label': 'Nombre', 'tipo': 'text'},
            {'name': 'fecha_inicio', 'label': 'Fecha Inicio', 'tipo': 'date'},
            {'name': 'fecha_fin', 'label': 'Fecha Fin', 'tipo': 'date'},
            {'name': 'activo', 'label': 'Activo', 'tipo': 'checkbox'}
        ]
    })


def periodo_eliminar(request, pk):
    if request.method == 'POST':
        resultado = odoo_client.eliminar_registro('periodo', pk)
        if resultado.get('status') == 'success':
            messages.success(request, 'Período eliminado')
        else:
            messages.error(request, resultado.get('message'))
        return redirect('integracion:periodo_lista')
    return render(request, 'integracion/confirmar_eliminar.html', {
        'titulo': 'Eliminar Período',
        'modelo': 'periodo',
        'id': pk
    })


# ============================================================
# MODELO: AULA
# ============================================================

def aula_lista(request):
    resultado = odoo_client.obtener_todos('aula')
    registros = resultado.get('data', []) if resultado.get('status') == 'success' else []
    if resultado.get('status') == 'error':
        messages.error(request, resultado.get('message'))
    return render(request, 'integracion/lista.html', {
        'titulo': 'Aulas',
        'modelo': 'aula',
        'registros': registros,
        'campos': ['id', 'name', 'edificio', 'capacidad']
    })


def aula_crear(request):
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'edificio': request.POST.get('edificio'),
            'capacidad': int(request.POST.get('capacidad', 30))
        }
        resultado = odoo_client.crear_registro('aula', data)
        if resultado.get('status') == 'success':
            messages.success(request, 'Aula creada exitosamente')
            return redirect('integracion:aula_lista')
        else:
            messages.error(request, resultado.get('message'))
    return render(request, 'integracion/form_crear.html', {
        'titulo': 'Nueva Aula',
        'modelo': 'aula',
        'campos': [
            {'name': 'name', 'label': 'Nombre', 'tipo': 'text'},
            {'name': 'edificio', 'label': 'Edificio', 'tipo': 'text'},
            {'name': 'capacidad', 'label': 'Capacidad', 'tipo': 'number'}
        ]
    })


def aula_eliminar(request, pk):
    if request.method == 'POST':
        resultado = odoo_client.eliminar_registro('aula', pk)
        if resultado.get('status') == 'success':
            messages.success(request, 'Aula eliminada')
        else:
            messages.error(request, resultado.get('message'))
        return redirect('integracion:aula_lista')
    return render(request, 'integracion/confirmar_eliminar.html', {
        'titulo': 'Eliminar Aula',
        'modelo': 'aula',
        'id': pk
    })


# ============================================================
# MODELO: TEACHER (Docentes / sistema.usuarios)
# ============================================================

def teacher_lista(request):
    resultado = odoo_client.obtener_todos('teacher')
    registros = resultado.get('data', []) if resultado.get('status') == 'success' else []
    if resultado.get('status') == 'error':
        messages.error(request, resultado.get('message'))
    return render(request, 'integracion/lista.html', {
        'titulo': 'Docentes',
        'modelo': 'teacher',
        'registros': registros,
        'campos': ['id', 'name', 'last_name', 'email', 'phone', 'vat']
    })


def teacher_crear(request):
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'last_name': request.POST.get('last_name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'vat': request.POST.get('vat')
        }
        resultado = odoo_client.crear_registro('teacher', data)
        if resultado.get('status') == 'success':
            messages.success(request, 'Docente creado exitosamente')
            return redirect('integracion:teacher_lista')
        else:
            messages.error(request, resultado.get('message'))
    return render(request, 'integracion/form_crear.html', {
        'titulo': 'Nuevo Docente',
        'modelo': 'teacher',
        'campos': [
            {'name': 'name', 'label': 'Nombre', 'tipo': 'text'},
            {'name': 'last_name', 'label': 'Apellido', 'tipo': 'text'},
            {'name': 'email', 'label': 'Correo', 'tipo': 'email'},
            {'name': 'phone', 'label': 'Teléfono', 'tipo': 'text'},
            {'name': 'vat', 'label': 'CI/RUC', 'tipo': 'text'}
        ]
    })


def teacher_eliminar(request, pk):
    if request.method == 'POST':
        resultado = odoo_client.eliminar_registro('teacher', pk)
        if resultado.get('status') == 'success':
            messages.success(request, 'Docente eliminado')
        else:
            messages.error(request, resultado.get('message'))
        return redirect('integracion:teacher_lista')
    return render(request, 'integracion/confirmar_eliminar.html', {
        'titulo': 'Eliminar Docente',
        'modelo': 'teacher',
        'id': pk
    })


# ============================================================
# MODELO: SIGNATURE (Materias / ou.signature)
# ============================================================

def signature_lista(request):
    resultado = odoo_client.obtener_todos('signature')
    registros = resultado.get('data', []) if resultado.get('status') == 'success' else []
    if resultado.get('status') == 'error':
        messages.error(request, resultado.get('message'))
    return render(request, 'integracion/lista.html', {
        'titulo': 'Materias',
        'modelo': 'signature',
        'registros': registros,
        'campos': ['id', 'name']
    })


def signature_crear(request):
    if request.method == 'POST':
        data = {'name': request.POST.get('name')}
        resultado = odoo_client.crear_registro('signature', data)
        if resultado.get('status') == 'success':
            messages.success(request, 'Materia creada exitosamente')
            return redirect('integracion:signature_lista')
        else:
            messages.error(request, resultado.get('message'))
    return render(request, 'integracion/form_crear.html', {
        'titulo': 'Nueva Materia',
        'modelo': 'signature',
        'campos': [
            {'name': 'name', 'label': 'Nombre', 'tipo': 'text'}
        ]
    })


def signature_eliminar(request, pk):
    if request.method == 'POST':
        resultado = odoo_client.eliminar_registro('signature', pk)
        if resultado.get('status') == 'success':
            messages.success(request, 'Materia eliminada')
        else:
            messages.error(request, resultado.get('message'))
        return redirect('integracion:signature_lista')
    return render(request, 'integracion/confirmar_eliminar.html', {
        'titulo': 'Eliminar Materia',
        'modelo': 'signature',
        'id': pk
    })