from unittest.mock import patch

from django.test import SimpleTestCase
from django.urls import reverse


class IntegracionViewsTests(SimpleTestCase):
    def test_inicio(self):
        response = self.client.get(reverse("integracion:inicio"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Integración académica")

    @patch("integracion.views.obtener_todos")
    def test_lista_renderiza_registros(self, obtener_todos):
        obtener_todos.return_value = [{"id": 1, "name": "Software", "codigo": "TDS", "modalidad": "Presencial"}]
        response = self.client.get(reverse("integracion:lista", args=["carrera"]))
        self.assertContains(response, "Software")
        self.assertContains(response, "TDS")

    @patch("integracion.views.crear_registro")
    def test_crear_carrera(self, crear_registro):
        crear_registro.return_value = {"status": "success", "message": "Carrera creada"}
        response = self.client.post(reverse("integracion:crear", args=["carrera"]), {
            "name": "Software", "codigo": "TDS", "modalidad": "Presencial",
        })
        self.assertRedirects(response, reverse("integracion:lista", args=["carrera"]), fetch_redirect_response=False)
        crear_registro.assert_called_once()

    @patch("integracion.views.eliminar_registro")
    def test_eliminar(self, eliminar_registro):
        eliminar_registro.return_value = {"status": "success", "message": "Eliminado"}
        response = self.client.post(reverse("integracion:eliminar", args=["aula", 9]))
        self.assertRedirects(response, reverse("integracion:lista", args=["aula"]), fetch_redirect_response=False)
        eliminar_registro.assert_called_once_with("aula", 9)

    def test_modelo_desconocido_retorna_404(self):
        response = self.client.get("/integracion/desconocido/")
        self.assertEqual(response.status_code, 404)
