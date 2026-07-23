import logging
import requests

# Configuración del logger para capturar errores en consola
logger = logging.getLogger(__name__)

# Configuración base de la API de Odoo
ODOO_BASE_URL = "http://localhost:8069"
TIMEOUT = 5


def obtener_todos(modelo):
    """GET /api_ute/<modelo>/all -> retorna (registros: list, error: str/None)"""
    url = f"{ODOO_BASE_URL}/api_ute/{modelo}/all"
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()

        if data.get('status') == 'success':
            return data.get('data', []), None
        return [], data.get('message', 'Error desconocido en Odoo')

    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar a la URL: {url}")
        return [], "No se pudo conectar con Odoo"
    except requests.exceptions.Timeout:
        return [], "Tiempo de espera agotado al conectar con Odoo"
    except Exception as e:
        logger.exception("Error inesperado consultando Odoo")
        return [], str(e)


def crear_registro(modelo, data):
    """POST /api_ute/<modelo>/create -> retorna (ok: bool, mensaje: str)"""
    url = f"{ODOO_BASE_URL}/api_ute/{modelo}/create"
    try:
        response = requests.post(url, json=data, timeout=TIMEOUT)
        response.raise_for_status()
        result = response.json()

        if result.get('status') == 'success':
            return True, result.get('message', 'Registro creado con éxito')
        else:
            return False, result.get('message', 'Error al crear en Odoo')

    except requests.exceptions.ConnectionError:
        return False, "No se pudo conectar con Odoo"
    except Exception as e:
        logger.exception("Error creando registro en Odoo")
        return False, str(e)


def eliminar_registro(modelo, registro_id):
    """DELETE /api_ute/<modelo>/delete/<id> -> retorna (ok: bool, mensaje: str)"""
    url = f"{ODOO_BASE_URL}/api_ute/{modelo}/delete/{registro_id}"
    try:
        response = requests.delete(url, timeout=TIMEOUT)
        response.raise_for_status()
        result = response.json()

        if result.get('status') == 'success':
            return True, result.get('message', 'Registro eliminado con éxito')
        else:
            return False, result.get('message', 'Error al eliminar en Odoo')

    except requests.exceptions.ConnectionError:
        return False, "No se pudo conectar con Odoo"
    except Exception as e:
        logger.exception("Error eliminando registro en Odoo")
        return False, str(e)