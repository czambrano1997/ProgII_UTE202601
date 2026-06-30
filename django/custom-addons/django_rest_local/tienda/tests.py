from django.test import TestCase
from .models import Producto 
class ProductoModelTestCase(TestCase):
    def setUp(self):
        self.p = Producto.objects.create(
            nombre='Laptop',precio=89.99,stock=5
        )

def test_nombre_producto(self):
        self.assertEqual(self.p.nombre, 'Laptop')

# Create your tests here.
