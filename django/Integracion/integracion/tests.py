from django.test import TestCase
from .models import Cliente,Paquete
# Create your tests here.
class ClientesModelTest(TestCase):
    def setUp(self):
        cat = Cliente.objects.create(nombre = 'Tec',
        codigo = 'Tec')
        self.p = Paquete.objects.create(
            nombre = 'Producto',precio = 999,
            categoria = cat
        ) 
    def tes_nombre_correcto(self):
        self.assertEqual(self.p.nombre,'Producto')