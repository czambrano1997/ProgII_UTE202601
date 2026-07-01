"""Pruebas unitarias: cada test valida un modelo aislado (sin vistas ni HTTP)."""
from decimal import Decimal

from django.db import IntegrityError
from django.db.models import ProtectedError
from django.test import TestCase

from tienda.models import Categoria, FichaTecnica, Producto, Proveedor


class CategoriaModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nombre="Electrónica", codigo="ELEC", descripcion="Equipos electrónicos"
        )

    def test_str_incluye_codigo_y_nombre(self):
        self.assertEqual(str(self.categoria), "(ELEC) Electrónica")

    def test_activa_por_defecto(self):
        self.assertTrue(self.categoria.activa)

    def test_nombre_es_unico(self):
        with self.assertRaises(IntegrityError):
            Categoria.objects.create(nombre="Electrónica", codigo="ELEC2")


class ProveedorModelTest(TestCase):
    def test_pais_por_defecto_es_ecuador(self):
        proveedor = Proveedor.objects.create(nombre="Acme", contacto="acme@example.com")
        self.assertEqual(proveedor.pais, "Ecuador")

    def test_str_devuelve_nombre(self):
        proveedor = Proveedor.objects.create(nombre="Acme", contacto="acme2@example.com")
        self.assertEqual(str(proveedor), "Acme")


class ProductoModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Muebles", codigo="MUE")
        self.producto = Producto.objects.create(
            nombre="Silla", precio=Decimal("50.00"), existencias=10, categoria=self.categoria
        )

    def test_str_incluye_categoria(self):
        self.assertEqual(str(self.producto), "Silla (Muebles)")

    def test_relacion_fk_categoria(self):
        self.assertIn(self.producto, self.categoria.productos.all())

    def test_relacion_m2m_proveedores(self):
        proveedor = Proveedor.objects.create(nombre="Acme", contacto="m2m@example.com")
        self.producto.proveedores.add(proveedor)
        self.assertIn(proveedor, self.producto.proveedores.all())
        self.assertIn(self.producto, proveedor.productos.all())

    def test_no_se_puede_borrar_categoria_con_productos(self):
        with self.assertRaises(ProtectedError):
            self.categoria.delete()


class FichaTecnicaModelTest(TestCase):
    def setUp(self):
        categoria = Categoria.objects.create(nombre="Tecnología", codigo="TEC")
        self.producto = Producto.objects.create(
            nombre="Laptop", precio=Decimal("999.00"), categoria=categoria
        )

    def test_relacion_uno_a_uno(self):
        ficha = FichaTecnica.objects.create(producto=self.producto, peso_kg=Decimal("2.10"))
        self.assertEqual(self.producto.ficha_tecnica, ficha)

    def test_garantia_por_defecto(self):
        ficha = FichaTecnica.objects.create(producto=self.producto, peso_kg=Decimal("2.10"))
        self.assertEqual(ficha.garantia_meses, 12)

    def test_str(self):
        ficha = FichaTecnica.objects.create(producto=self.producto, peso_kg=Decimal("2.10"))
        self.assertEqual(str(ficha), "Ficha de Laptop")
