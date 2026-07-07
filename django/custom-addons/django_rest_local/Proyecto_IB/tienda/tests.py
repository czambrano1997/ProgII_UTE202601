from django.test import TestCase
from .models import Producto


class ProductoModelTest(TestCase):
    def setUp(self):
        self.producto = Producto.objects.create(nombre="Laptop", precio=999, stock=10)

    def test_nombre_producto(self):
        self.assertEqual(self.producto.nombre, "Laptop")

    def test_precio_producto(self):
        self.assertEqual(self.producto.precio, 999)

    def test_stock_producto(self):
        self.assertEqual(self.producto.stock, 10)

    def test_str_representation(self):
        self.assertEqual(str(self.producto), "Laptop")
