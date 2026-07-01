from datetime import date, timedelta
from decimal import Decimal

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import models
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import (
    Categoria,
    Cliente,
    DetallePedido,
    Pedido,
    Producto,
    Proveedor,
)


class DatosBaseMixin:
    @classmethod
    def setUpTestData(cls):
        cls.categoria = Categoria.objects.create(
            nombre="Tecnología",
            descripcion="Equipos y accesorios",
            slug="tecnologia",
        )

        cls.proveedor = Proveedor.objects.create(
            nombre="Proveedor Uno",
            correo="ventas@proveedor.test",
            telefono="0990000000",
            sitio_web="https://example.com",
        )

        cls.producto = Producto.objects.create(
            nombre="Teclado mecánico",
            sku="TEC-001",
            descripcion="Teclado para oficina",
            categoria=cls.categoria,
            proveedor=cls.proveedor,
            precio=Decimal("50.00"),
            stock=8,
            stock_minimo=3,
            slug="teclado-mecanico",
        )

        cls.cliente = Cliente.objects.create(
            nombres="Ana",
            apellidos="Pérez",
            correo="ana@example.com",
            telefono="0980000000",
            direccion="Quito",
            fecha_nacimiento=date(2000, 1, 10),
        )

        cls.pedido = Pedido.objects.create(
            codigo="PED-001",
            cliente=cls.cliente,
            estado=Pedido.Estado.PAGADO,
        )

        cls.detalle = DetallePedido.objects.create(
            pedido=cls.pedido,
            producto=cls.producto,
            cantidad=2,
            precio_unitario=Decimal("50.00"),
            descuento=Decimal("10.00"),
        )


class ModelosYRelacionesTests(DatosBaseMixin, TestCase):
    def test_existen_seis_modelos_principales(self):
        self.assertEqual(Categoria.objects.count(), 1)
        self.assertEqual(Proveedor.objects.count(), 1)
        self.assertEqual(Producto.objects.count(), 1)
        self.assertEqual(Cliente.objects.count(), 1)
        self.assertEqual(Pedido.objects.count(), 1)
        self.assertEqual(DetallePedido.objects.count(), 1)

    def test_relaciones_foreign_key(self):
        self.assertEqual(
            self.producto.categoria,
            self.categoria,
        )

        self.assertEqual(
            self.producto.proveedor,
            self.proveedor,
        )

        self.assertEqual(
            self.pedido.cliente,
            self.cliente,
        )

    def test_relacion_muchos_a_muchos_con_modelo_intermedio(self):
        self.assertIn(
            self.producto,
            self.pedido.productos.all(),
        )

        self.assertIn(
            self.pedido,
            self.producto.pedidos.all(),
        )

    def test_subtotal_con_descuento(self):
        self.assertEqual(
            self.detalle.subtotal,
            Decimal("90.00"),
        )

        self.assertEqual(
            self.pedido.total,
            Decimal("90.00"),
        )

    def test_stock_bajo(self):
        self.producto.stock = 3

        self.assertTrue(
            self.producto.necesita_reposicion
        )

    def test_tipos_de_campos(self):
        self.assertIsInstance(
            Producto._meta.get_field("nombre"),
            models.CharField,
        )

        self.assertIsInstance(
            Producto._meta.get_field("descripcion"),
            models.TextField,
        )

        self.assertIsInstance(
            Proveedor._meta.get_field("correo"),
            models.EmailField,
        )

        self.assertIsInstance(
            Cliente._meta.get_field("fecha_nacimiento"),
            models.DateField,
        )

        self.assertIsInstance(
            Producto._meta.get_field("fecha_creacion"),
            models.DateTimeField,
        )

        self.assertIsInstance(
            Producto._meta.get_field("disponible"),
            models.BooleanField,
        )

        self.assertIsInstance(
            Producto._meta.get_field("stock"),
            models.PositiveIntegerField,
        )

        self.assertIsInstance(
            Producto._meta.get_field("precio"),
            models.DecimalField,
        )

        self.assertIsInstance(
            Proveedor._meta.get_field("sitio_web"),
            models.URLField,
        )

        self.assertIsInstance(
            Producto._meta.get_field("slug"),
            models.SlugField,
        )

        self.assertIsInstance(
            Producto._meta.get_field("categoria"),
            models.ForeignKey,
        )

        self.assertIsInstance(
            Pedido._meta.get_field("productos"),
            models.ManyToManyField,
        )

    def test_edad_se_calcula_desde_fecha_nacimiento(self):
        hoy = timezone.localdate()
        nacimiento = date(2000, 1, 1)

        edad_esperada = hoy.year - nacimiento.year - (
            (hoy.month, hoy.day)
            < (nacimiento.month, nacimiento.day)
        )

        self.cliente.fecha_nacimiento = nacimiento

        self.assertEqual(
            self.cliente.edad,
            edad_esperada,
        )

    def test_rechaza_fecha_nacimiento_futura(self):
        self.cliente.fecha_nacimiento = (
            timezone.localdate() + timedelta(days=1)
        )

        with self.assertRaises(ValidationError):
            self.cliente.full_clean()

    def test_rechaza_cliente_menor_de_edad(self):
        hoy = timezone.localdate()

        self.cliente.fecha_nacimiento = (
            hoy - timedelta(days=365 * 10)
        )

        with self.assertRaises(ValidationError):
            self.cliente.full_clean()

    def test_rechaza_nombres_con_numeros(self):
        self.cliente.nombres = "Ana123"

        with self.assertRaises(ValidationError):
            self.cliente.full_clean()

    def test_rechaza_telefono_invalido(self):
        self.cliente.telefono = "09A-123"

        with self.assertRaises(ValidationError):
            self.cliente.full_clean()


class VistasTests(DatosBaseMixin, TestCase):
    rutas = {
        "djangov1:inicio": "djangov1/inicio.html",
        "djangov1:categorias": "djangov1/categorias.html",
        "djangov1:proveedores": "djangov1/proveedores.html",
        "djangov1:productos": "djangov1/productos.html",
        "djangov1:clientes": "djangov1/clientes.html",
        "djangov1:pedidos": "djangov1/pedidos.html",
        "djangov1:detalles_pedido": (
            "djangov1/detalles_pedido.html"
        ),
    }

    def test_todas_las_vistas_responden(self):
        for nombre_ruta, plantilla in self.rutas.items():
            with self.subTest(nombre_ruta=nombre_ruta):
                respuesta = self.client.get(
                    reverse(nombre_ruta)
                )

                self.assertEqual(
                    respuesta.status_code,
                    200,
                )

                self.assertTemplateUsed(
                    respuesta,
                    plantilla,
                )

    def test_lista_productos_muestra_datos(self):
        respuesta = self.client.get(
            reverse("djangov1:productos")
        )

        self.assertContains(
            respuesta,
            "Teclado mecánico",
        )

        self.assertContains(
            respuesta,
            "TEC-001",
        )

    def test_lista_pedidos_muestra_total(self):
        respuesta = self.client.get(
            reverse("djangov1:pedidos")
        )

        self.assertContains(
            respuesta,
            "PED-001",
        )

        self.assertContains(
            respuesta,
            "90,00",
        )


class AdminTests(TestCase):
    def test_los_seis_modelos_estan_registrados(self):
        modelos = (
            Categoria,
            Proveedor,
            Producto,
            Cliente,
            Pedido,
            DetallePedido,
        )

        for modelo in modelos:
            with self.subTest(modelo=modelo.__name__):
                self.assertIn(
                    modelo,
                    admin.site._registry,
                )


class ComandoDatosDemoTests(TestCase):
    def test_comando_es_repetible(self):
        call_command(
            "cargar_datos_demo",
            verbosity=0,
        )

        call_command(
            "cargar_datos_demo",
            verbosity=0,
        )

        self.assertGreaterEqual(
            Categoria.objects.count(),
            3,
        )

        self.assertGreaterEqual(
            Producto.objects.count(),
            5,
        )

        self.assertGreaterEqual(
            Cliente.objects.count(),
            2,
        )

        self.assertGreaterEqual(
            Pedido.objects.count(),
            2,
        )

        self.assertGreaterEqual(
            DetallePedido.objects.count(),
            3,
        )


class ComandoAdminTests(TestCase):
    def test_prepara_usuario_emily_sin_exponer_password(self):
        call_command(
            "preparar_admin_emily",
            verbosity=0,
        )

        usuario = get_user_model().objects.get(
            username="emily"
        )

        self.assertTrue(
            usuario.is_staff
        )

        self.assertTrue(
            usuario.is_superuser
        )

        self.assertFalse(
            usuario.has_usable_password()
        )
