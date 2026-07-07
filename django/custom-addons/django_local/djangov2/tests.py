from django.test import SimpleTestCase
from django.urls import resolve


class ApiRoutesTests(SimpleTestCase):
    def test_autores_api_route_is_registered(self):
        match = resolve("/api/autores/")
        self.assertEqual(match.view_name, "autor-list")
