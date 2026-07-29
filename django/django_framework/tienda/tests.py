from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Categoria, Cliente, Producto


class ApiEndpointsTests(APITestCase):
    def test_api_root_expone_los_endpoints_principales(self):
        url = reverse("api-root")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("categorias", response.data)
        self.assertIn("clientes", response.data)
        self.assertIn("productos", response.data)

    def test_listado_de_categorias_y_clientes(self):
        Categoria.objects.create(nombre="Tecnología")
        Cliente.objects.create(nombre="Ana", email="ana@test.com")

        categorias_response = self.client.get(reverse("categoria-list"))
        clientes_response = self.client.get(reverse("cliente-list"))

        self.assertEqual(categorias_response.status_code, status.HTTP_200_OK)
        self.assertEqual(clientes_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(categorias_response.data), 1)
        self.assertEqual(len(clientes_response.data), 1)

    def test_crear_producto_via_api(self):
        categoria = Categoria.objects.create(nombre="Tecnología")
        url = reverse("producto-list")
        payload = {"nombre": "Mouse", "precio": "15.50", "stock": 10, "categoria": categoria.id}

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Producto.objects.count(), 1)
        self.assertEqual(Producto.objects.get().nombre, "Mouse")
