"""Pruebas de integración (viewset + BD) y funcionales/E2E (seguridad + flujo completo) sobre la API DRF."""
from decimal import Decimal

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from tienda.models import Categoria, Producto

PRODUCTOS_URL = "/api/productos/"


class ProductoListaPublicaTest(APITestCase):
    """Integración: lectura pública (IsAuthenticatedOrReadOnly permite GET anónimo)."""

    def setUp(self):
        categoria = Categoria.objects.create(nombre="Periféricos", codigo="PER")
        Producto.objects.create(nombre="Teclado", precio=Decimal("25.00"), categoria=categoria)

    def test_listar_sin_autenticar_devuelve_200(self):
        resp = self.client.get(PRODUCTOS_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)

    def test_listar_incluye_el_producto_creado(self):
        resp = self.client.get(PRODUCTOS_URL)
        self.assertContains(resp, "Teclado")


class ProductoSeguridadTest(APITestCase):
    """Seguridad: sin token/sesión no se puede escribir."""

    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Accesorios", codigo="ACC")

    def test_crear_sin_autenticar_es_rechazado(self):
        resp = self.client.post(PRODUCTOS_URL, {
            "nombre": "Mouse", "precio": "10.00", "existencias": 5, "categoria": self.categoria.id,
        })
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
        self.assertEqual(Producto.objects.count(), 0)


class ProductoFlujoCompletoTest(APITestCase):
    """Funcional/E2E: login -> crear -> verificar en el listado."""

    def setUp(self):
        self.user = User.objects.create_user(username="ana", password="clave123")
        self.categoria = Categoria.objects.create(nombre="Accesorios", codigo="ACC")

    def test_usuario_autenticado_crea_producto_y_lo_ve_en_lista(self):
        self.client.force_authenticate(user=self.user)

        resp_crear = self.client.post(PRODUCTOS_URL, {
            "nombre": "Mouse", "precio": "10.00", "existencias": 5, "categoria": self.categoria.id,
        })
        self.assertEqual(resp_crear.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Producto.objects.count(), 1)

        resp_lista = self.client.get(PRODUCTOS_URL)
        self.assertContains(resp_lista, "Mouse")

    def test_crear_con_precio_invalido_devuelve_400(self):
        self.client.force_authenticate(user=self.user)
        resp = self.client.post(PRODUCTOS_URL, {
            "nombre": "Malo", "precio": "0", "existencias": 1, "categoria": self.categoria.id,
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Producto.objects.count(), 0)
