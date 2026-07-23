from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from integracion.odoo_client import OdooClientError, OdooNoDisponible, crear_registro, eliminar_registro, obtener_todos


class OdooClientTests(SimpleTestCase):
    @patch("integracion.odoo_client.requests.request")
    def test_obtener_todos(self, mock_request):
        response = Mock(ok=True, status_code=200)
        response.json.return_value = {"status": "success", "data": [{"id": 1, "name": "Programación II"}]}
        mock_request.return_value = response
        self.assertEqual(obtener_todos("signature")[0]["name"], "Programación II")
        mock_request.assert_called_once()

    @patch("integracion.odoo_client.requests.request")
    def test_crear_registro(self, mock_request):
        response = Mock(ok=True, status_code=201)
        response.json.return_value = {"status": "success", "message": "Creado", "data": {"id": 3}}
        mock_request.return_value = response
        self.assertEqual(crear_registro("aula", {"name": "101", "edificio": "A", "capacidad": 20})["data"]["id"], 3)

    @patch("integracion.odoo_client.requests.request")
    def test_eliminar_registro(self, mock_request):
        response = Mock(ok=True, status_code=200)
        response.json.return_value = {"status": "success", "message": "Eliminado", "data": {"id": 3}}
        mock_request.return_value = response
        self.assertEqual(eliminar_registro("aula", 3)["status"], "success")

    @patch("integracion.odoo_client.requests.request")
    def test_error_api(self, mock_request):
        response = Mock(ok=False, status_code=400)
        response.json.return_value = {"status": "error", "message": "Datos inválidos"}
        mock_request.return_value = response
        with self.assertRaisesMessage(OdooClientError, "Datos inválidos"):
            crear_registro("carrera", {})

    @patch("integracion.odoo_client.requests.request")
    def test_odoo_no_disponible(self, mock_request):
        import requests
        mock_request.side_effect = requests.ConnectionError("sin conexión")
        with self.assertRaises(OdooNoDisponible):
            obtener_todos("periodo")
