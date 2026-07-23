import os
from typing import Any

import requests

ODOO_BASE_URL = os.getenv("ODOO_BASE_URL", "http://localhost:8069").rstrip("/")
ODOO_TIMEOUT = float(os.getenv("ODOO_TIMEOUT", "10"))
MODELOS_VALIDOS = {"signature", "usuarios", "carrera", "periodo", "aula"}


class OdooClientError(Exception):
    """Error controlado de comunicación o respuesta de Odoo."""


class OdooNoDisponible(OdooClientError):
    """Odoo no respondió o no fue accesible."""


def _validar_modelo(modelo: str) -> None:
    if modelo not in MODELOS_VALIDOS:
        raise ValueError(f"Modelo no soportado: {modelo}")


def _request(method: str, path: str, **kwargs: Any) -> dict:
    url = f"{ODOO_BASE_URL}{path}"
    try:
        response = requests.request(method, url, timeout=ODOO_TIMEOUT, **kwargs)
    except (requests.ConnectionError, requests.Timeout) as exc:
        raise OdooNoDisponible("No se pudo conectar con Odoo. Verifica que esté activo en el puerto 8069.") from exc
    except requests.RequestException as exc:
        raise OdooClientError(f"Error al comunicarse con Odoo: {exc}") from exc

    try:
        payload = response.json()
    except ValueError as exc:
        raise OdooClientError(f"Odoo respondió HTTP {response.status_code}, pero no devolvió JSON válido.") from exc

    if not isinstance(payload, dict):
        raise OdooClientError("La respuesta de Odoo no tiene el formato esperado.")

    if not response.ok or payload.get("status") != "success":
        message = payload.get("message") or f"Odoo respondió con HTTP {response.status_code}."
        raise OdooClientError(str(message))
    return payload


def obtener_todos(modelo: str) -> list[dict]:
    """GET /api_ute/<modelo>/all y retorna la lista de registros."""
    _validar_modelo(modelo)
    payload = _request("GET", f"/api_ute/{modelo}/all")
    data = payload.get("data", [])
    if not isinstance(data, list):
        raise OdooClientError("Odoo devolvió un campo 'data' inválido.")
    return data


def crear_registro(modelo: str, data: dict) -> dict:
    """POST /api_ute/<modelo>/create enviando JSON."""
    _validar_modelo(modelo)
    return _request("POST", f"/api_ute/{modelo}/create", json=data)


def eliminar_registro(modelo: str, registro_id: int) -> dict:
    """DELETE /api_ute/<modelo>/delete/<id>."""
    _validar_modelo(modelo)
    return _request("DELETE", f"/api_ute/{modelo}/delete/{int(registro_id)}")
