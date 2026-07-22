import requests
import logging

_logger = logging.getLogger(__name__)

ODOO_BASE_URL = "http://localhost:8069"
TIMEOUT = 5


def obtener_todos(modelo):
    """Consulta registros enviando un GET a /api_ute/{modelo}/all"""
    url = f"{ODOO_BASE_URL}/api_ute/{modelo}/all"
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'success':
            return data.get('data', []), None
        return [], data.get('message', 'Error al obtener registros')

    except requests.exceptions.ConnectionError:
        _logger.error(f"No se pudo conectar con Odoo en {url}")
        return [], "No se pudo conectar con Odoo"
    except requests.exceptions.Timeout:
        return [], "Odoo tardó demasiado en responder"
    except Exception as e:
        _logger.exception("Error inesperado consultando Odoo")
        return [], str(e)


def crear_registro(modelo, data):
    """Crea un registro enviando un POST con JSON puro a /api_ute/{modelo}/create"""
    url = f"{ODOO_BASE_URL}/api_ute/{modelo}/create"
    try:
        # Petición POST REST enviando json nativo
        response = requests.post(url, json=data, timeout=TIMEOUT)
        response.raise_for_status()
        result = response.json()

        if result.get('status') == 'success':
            return True, result.get('message', 'Registro creado exitosamente')
        return False, result.get('message', 'Error al crear en Odoo')

    except requests.exceptions.ConnectionError:
        return False, "No se pudo conectar con Odoo"
    except Exception as e:
        _logger.exception("Error creando registro en Odoo")
        return False, str(e)


def eliminar_registro(modelo, registro_id):
    """Elimina un registro enviando un DELETE a /api_ute/{modelo}/delete/{id}"""
    url = f"{ODOO_BASE_URL}/api_ute/{modelo}/delete/{registro_id}"
    try:
        response = requests.delete(url, timeout=TIMEOUT)
        response.raise_for_status()
        result = response.json()

        if result.get('status') == 'success':
            return True, result.get('message', 'Registro eliminado')
        return False, result.get('message', 'Error al eliminar')

    except requests.exceptions.ConnectionError:
        return False, "No se pudo conectar con Odoo"
    except Exception as e:
        _logger.exception("Error eliminando registro en Odoo")
        return False, str(e)