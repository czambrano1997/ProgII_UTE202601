from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Producto


class ProductoApiTests(APITestCase):
    def test_listado_de_productos_vacio(self):
        url = reverse("producto-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_crear_producto_via_api(self):
        url = reverse("producto-list")
        payload = {"nombre": "Mouse", "precio": "15.50", "stock": 10}

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Producto.objects.count(), 1)
        self.assertEqual(Producto.objects.get().nombre, "Mouse")
