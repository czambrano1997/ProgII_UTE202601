from django.shortcuts import render, redirect
from django.contrib import messages
from . import odoo_client

# Configuración mapeada exactamente desde las respuestas (fields y vals) de tus Controladores de Odoo
MODELOS_CONFIG = {
    'signature': {
        'nombre_display': 'Materias',
        'campos': ['id', 'name'],
        'campos_form': ['name'],
    },
    'techers': {
        'nombre_display': 'Docentes',
        'campos': ['id', 'name', 'last_name', 'email', 'phone', 'vat', 'validate_email', 'signature_primary'],
        'campos_form': ['name', 'last_name', 'email', 'phone', 'vat', 'signature_primary'],
    },
    'book_loan': {
        'nombre_display': 'Préstamo de Libros',
        'campos': ['id', 'name', 'book', 'book_gender', 'loan_date', 'book_observations'],
        'campos_form': ['student_id', 'book_id', 'loan_date', 'book_observations'],
    },
    'estudiantes': {
        'nombre_display': 'Estudiantes',
        'campos': ['id', 'name', 'surnames', 'age', 'phone', 'vat'],
        'campos_form': ['name', 'surnames', 'age', 'phone', 'vat'],
    },
    'library': {
        'nombre_display': 'Libros',
        'campos': ['id', 'name', 'author', 'headquarters', 'hous', 'gender', 'income'],
        'campos_form': ['name', 'author', 'headquarters', 'hous', 'gender', 'income'],
    },
}


def lista(request, modelo):
    config = MODELOS_CONFIG.get(modelo)
    if not config:
        messages.error(request, f"Modelo '{modelo}' no reconocido")
        return redirect('integracion:lista', modelo='library')
    
    registros, error = odoo_client.obtener_todos(modelo)
    if error:
        messages.error(request, error)
        
    return render(request, 'integracion/lista.html', {
        'modelo': modelo,
        'nombre_display': config['nombre_display'],
        'campos': config['campos'],
        'registros': registros or [],
        'modelos_disponibles': MODELOS_CONFIG,
    })


def crear(request, modelo):
    config = MODELOS_CONFIG.get(modelo)
    if not config:
        messages.error(request, f"Modelo '{modelo}' no reconocido")
        return redirect('integracion:lista', modelo='library')
    
    if request.method == 'POST':
        data = {campo: request.POST.get(campo) for campo in config['campos_form']}
        ok, mensaje = odoo_client.crear_registro(modelo, data)
        if ok:
            messages.success(request, mensaje)
            return redirect('integracion:lista', modelo=modelo)
        else:
            messages.error(request, mensaje)
            
    return render(request, 'integracion/form.html', {
        'modelo': modelo,
        'nombre_display': config['nombre_display'],
        'campos_form': config['campos_form'],
        'modelos_disponibles': MODELOS_CONFIG,
    })


def confirmar_eliminar(request, modelo, registro_id):
    config = MODELOS_CONFIG.get(modelo)
    if not config:
        messages.error(request, f"Modelo '{modelo}' no reconocido")
        return redirect('integracion:lista', modelo='library')
    
    if request.method == 'POST':
        ok, mensaje = odoo_client.eliminar_registro(modelo, registro_id)
        if ok:
            messages.success(request, mensaje)
        else:
            messages.error(request, mensaje)
        return redirect('integracion:lista', modelo=modelo)
        
    return render(request, 'integracion/confirmar_eliminar.html', {
        'modelo': modelo,
        'nombre_display': config['nombre_display'],
        'registro_id': registro_id,
        'modelos_disponibles': MODELOS_CONFIG,
    })