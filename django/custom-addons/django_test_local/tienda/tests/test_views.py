"""Pruebas de integración (vista + BD) y funcionales (petición HTTP completa) sobre MVT."""
from decimal import Decimal

from django.test import Client, TestCase
from django.urls import reverse

from tienda.models import Categoria, Producto


class CategoriaViewTest(TestCase):
    """Integración: la vista consulta la BD real y arma el contexto correcto."""

    def setUp(self):
        self.client = Client()
        Categoria.objects.create(nombre="Ropa", codigo="ROP")
        Categoria.objects.create(nombre="Hogar", codigo="HOG")

    def test_responde_200(self):
        resp = self.client.get(reverse("tienda:categoria"))
        self.assertEqual(resp.status_code, 200)

    def test_usa_el_template_esperado(self):
        resp = self.client.get(reverse("tienda:categoria"))
        self.assertTemplateUsed(resp, "tienda/categoria.html")

    def test_contenido_incluye_las_categorias_creadas(self):
        resp = self.client.get(reverse("tienda:categoria"))
        self.assertContains(resp, "Ropa")
        self.assertContains(resp, "Hogar")

    def test_contexto_total_coincide_con_la_bd(self):
        resp = self.client.get(reverse("tienda:categoria"))
        self.assertEqual(resp.context["total"], 2)

    def test_lista_vacia_muestra_mensaje(self):
        Categoria.objects.all().delete()
        resp = self.client.get(reverse("tienda:categoria"))
        self.assertContains(resp, "No hay categorías registradas")


class ProductoViewTest(TestCase):
    """Integración: valida el select_related/prefetch_related contra la BD."""

    def setUp(self):
        self.client = Client()
        self.categoria = Categoria.objects.create(nombre="Electrónica", codigo="ELEC")
        Producto.objects.create(
            nombre="Teclado", precio=Decimal("25.00"), existencias=8, categoria=self.categoria
        )

    def test_responde_200(self):
        resp = self.client.get(reverse("tienda:lista_productos"))
        self.assertEqual(resp.status_code, 200)

    def test_contenido_incluye_producto_y_categoria(self):
        resp = self.client.get(reverse("tienda:lista_productos"))
        self.assertContains(resp, "Teclado")
        self.assertContains(resp, "Electrónica")

    def test_contexto_trae_los_productos_de_la_bd(self):
        resp = self.client.get(reverse("tienda:lista_productos"))
        productos = list(resp.context["productos"])
        self.assertEqual(len(productos), 1)
        self.assertEqual(productos[0].categoria.nombre, "Electrónica")

    def test_contexto_total_coincide_con_la_bd(self):
        resp = self.client.get(reverse("tienda:lista_productos"))
        self.assertEqual(resp.context["total"], 1)


class FlujoNavegacionTest(TestCase):
    """Funcional/E2E simple: recorre las dos páginas como lo haría un usuario."""

    def setUp(self):
        self.client = Client()
        categoria = Categoria.objects.create(nombre="Deportes", codigo="DEP")
        Producto.objects.create(nombre="Balón", precio=Decimal("15.00"), categoria=categoria)

    def test_usuario_ve_categorias_y_luego_productos(self):
        resp_categorias = self.client.get(reverse("tienda:categoria"))
        self.assertContains(resp_categorias, "Deportes")

        resp_productos = self.client.get(reverse("tienda:lista_productos"))
        self.assertContains(resp_productos, "Balón")
