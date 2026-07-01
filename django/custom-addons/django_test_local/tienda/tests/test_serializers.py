"""Pruebas unitarias del serializer: validación de datos sin pasar por HTTP."""
from decimal import Decimal

from django.test import TestCase

from tienda.models import Categoria, Producto
from tienda.serializers import ProductoSerializer


class ProductoSerializerTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Cómputo", codigo="COMP")

    def test_serializa_los_campos_esperados(self):
        producto = Producto.objects.create(
            nombre="Monitor", precio=Decimal("150.00"), existencias=3, categoria=self.categoria
        )
        data = ProductoSerializer(producto).data
        self.assertEqual(set(data.keys()), {"id", "nombre", "precio", "existencias", "categoria"})
        self.assertEqual(data["nombre"], "Monitor")

    def test_precio_positivo_es_valido(self):
        serializer = ProductoSerializer(data={
            "nombre": "Silla", "precio": "50.00", "existencias": 1, "categoria": self.categoria.id,
        })
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_precio_cero_es_invalido(self):
        serializer = ProductoSerializer(data={
            "nombre": "Silla", "precio": "0.00", "existencias": 1, "categoria": self.categoria.id,
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn("precio", serializer.errors)

    def test_precio_negativo_es_invalido(self):
        serializer = ProductoSerializer(data={
            "nombre": "Silla", "precio": "-5.00", "existencias": 1, "categoria": self.categoria.id,
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn("precio", serializer.errors)
