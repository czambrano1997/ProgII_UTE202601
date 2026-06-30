from django.test import TestCase,Client
from .models import Producto

# Pruebas Unitarias
class ProductoModelTest(TestCase):
    def setUp(self):
        self.p=Producto.objects.create(
            nombre='Laptop',precio=999,stock=5)
        
    def test_nombre_correcto(self):
        self.assertEqual(self.p.nombre,'Laptop')

# Pruebas funcionales

class ProductoViewTest(TestCase):
    def setUp(self):
        self.client = Client