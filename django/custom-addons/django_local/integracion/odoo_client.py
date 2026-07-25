"""Cliente HTTP para comunicación con Odoo vía controladores REST.

Uso:
    from .odoo_client import obtener_todos, crear_registro, eliminar_registro

    # Listar
    resultado = obtener_todos('carrera')

    # Crear
    resultado = crear_registro('carrera', {'name': 'Software', 'codigo': 'TSW'})

    # Eliminar
    resultado = eliminar_registro('carrera', 5)
"""
import requests
import json

ODOO_BASE_URL = "http://localhost:8069"


def obtener_todos(modelo):
    """GET /api_ute/<modelo>/all → retorna lista de dicts."""
    try:
        url = f"{ODOO_BASE_URL}/api_ute/{modelo}/all"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {'status': 'error', 'message': 'No se pudo conectar con Odoo. Verifique que el servidor esté corriendo en el puerto 8069.'}
    except requests.exceptions.Timeout:
        return {'status': 'error', 'message': 'Tiempo de espera agotado al conectar con Odoo.'}
    except requests.exceptions.RequestException as e:
        return {'status': 'error', 'message': f'Error de conexión con Odoo: {str(e)}'}


def crear_registro(modelo, data):
    """POST /api_ute/<modelo>/create → envía JSON, retorna respuesta."""
    try:
        url = f"{ODOO_BASE_URL}/api_ute/{modelo}/create"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(data), headers=headers, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {'status': 'error', 'message': 'No se pudo conectar con Odoo. Verifique que el servidor esté corriendo en el puerto 8069.'}
    except requests.exceptions.Timeout:
        return {'status': 'error', 'message': 'Tiempo de espera agotado al conectar con Odoo.'}
    except requests.exceptions.RequestException as e:
        return {'status': 'error', 'message': f'Error de conexión con Odoo: {str(e)}'}


def eliminar_registro(modelo, registro_id):
    """DELETE /api_ute/<modelo>/delete/<id> → retorna respuesta."""
    try:
        url = f"{ODOO_BASE_URL}/api_ute/{modelo}/delete/{registro_id}"
        response = requests.delete(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {'status': 'error', 'message': 'No se pudo conectar con Odoo. Verifique que el servidor esté corriendo en el puerto 8069.'}
    except requests.exceptions.Timeout:
        return {'status': 'error', 'message': 'Tiempo de espera agotado al conectar con Odoo.'}
    except requests.exceptions.RequestException as e:
        return {'status': 'error', 'message': f'Error de conexión con Odoo: {str(e)}'}