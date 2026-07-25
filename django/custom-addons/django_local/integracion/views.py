from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from . import odoo_client

MODEL_CONFIG = {
    'signature': {
        'label': 'Materia',
        'fields': [
            {'name': 'name', 'label': 'Nombre'},
        ],
    },
    'usuarios': {
        'label': 'Usuario',
        'fields': [
            {'name': 'name', 'label': 'Nombre'},
            {'name': 'last_name', 'label': 'Apellido'},
            {'name': 'email', 'label': 'Correo'},
            {'name': 'phone', 'label': 'Teléfono'},
            {'name': 'vat', 'label': 'CI/RUC'},
        ],
    },
    'carrera': {
        'label': 'Carrera',
        'fields': [
            {'name': 'name', 'label': 'Nombre'},
            {'name': 'codigo', 'label': 'Código'},
            {'name': 'modalidad', 'label': 'Modalidad'},
        ],
    },
    'periodo': {
        'label': 'Periodo',
        'fields': [
            {'name': 'name', 'label': 'Nombre'},
            {'name': 'fecha_inicio', 'label': 'Fecha inicio'},
            {'name': 'fecha_fin', 'label': 'Fecha fin'},
            {'name': 'activo', 'label': 'Activo'},
        ],
    },
    'aula': {
        'label': 'Aula',
        'fields': [
            {'name': 'name', 'label': 'Nombre'},
            {'name': 'edificio', 'label': 'Edificio'},
            {'name': 'capacidad', 'label': 'Capacidad'},
        ],
    },
}


def get_model_config(model):
    config = MODEL_CONFIG.get(model)
    if not config:
        raise Http404('Modelo no encontrado')
    return config


def lista(request, model):
    config = get_model_config(model)
    result = odoo_client.obtener_todos(model)
    if result.get('error'):
        messages.error(request, result['error'])
    return render(request, 'integracion/lista.html', {
        'model': model,
        'label': config['label'],
        'fields': config['fields'],
        'registros': result.get('data', []),
    })


def crear(request, model):
    config = get_model_config(model)
    if request.method == 'POST':
        data = {field['name']: request.POST.get(field['name'], '').strip() for field in config['fields']}
        result = odoo_client.crear_registro(model, data)
        if result.get('error'):
            messages.error(request, result['error'])
        else:
            messages.success(request, f"{config['label']} creado correctamente")
            return redirect('integracion_lista', model=model)
    return render(request, 'integracion/form.html', {
        'model': model,
        'label': config['label'],
        'fields': config['fields'],
    })


def eliminar(request, model, record_id):
    config = get_model_config(model)
    if request.method == 'POST':
        result = odoo_client.eliminar_registro(model, record_id)
        if result.get('error'):
            messages.error(request, result['error'])
            return redirect('integracion_lista', model=model)
        messages.success(request, f"{config['label']} eliminado correctamente")
        return redirect('integracion_lista', model=model)

    registros = odoo_client.obtener_todos(model).get('data', [])
    registro = next((item for item in registros if item.get('id') == record_id), None)
    return render(request, 'integracion/confirmar_eliminar.html', {
        'model': model,
        'label': config['label'],
        'registro': registro or {'id': record_id},
    })
