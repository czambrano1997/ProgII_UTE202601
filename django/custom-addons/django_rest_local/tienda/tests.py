from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Producto


class ProductoModelTest(TestCase):
    def setUp(self):
        self.p = Producto.objects.create(nombre="Laptop", precio=999, stock=5)

    def test_nombre_correcto(self):
        self.assertEqual(self.p.nombre, "Laptop")


class ProductoApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_crear_producto_via_api(self):
        url = reverse("lista_productos")
        data = {"nombre": "Teclado", "precio": "19.99", "stock": 10}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Producto.objects.count(), 1)
        self.assertEqual(Producto.objects.get().nombre, "Teclado")

    def test_eliminar_producto_via_api(self):
        producto = Producto.objects.create(nombre="Mouse", precio="10.50", stock=2)
        url = reverse("detalle_producto", args=[producto.pk])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Producto.objects.count(), 0)

    def test_ruta_crear_muestra_formulario(self):
        url = reverse("crear_producto")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "nombre")
        self.assertContains(response, "precio")
        self.assertContains(response, "stock")

    def test_ruta_singular_muestra_detalle(self):
        producto = Producto.objects.create(nombre="Bateria", precio="15.50", stock=7)
        url = reverse("detalle_producto_singular", args=[producto.pk])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bateria")

    def test_crear_producto_desde_formulario_html(self):
        client = Client()
        url = reverse("crear_producto")

        response = client.post(
            url,
            {"nombre": "Formulario", "precio": "9.99", "stock": 4},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Producto.objects.filter(nombre="Formulario").exists())
