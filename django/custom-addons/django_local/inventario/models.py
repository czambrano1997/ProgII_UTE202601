from django.db import models

# Create your models here.
class Proveedor(models.Model):
    nombre_empresa = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    activo = models.BooleanField(default=True)
    def __str__(self): return self.nombre_empresa

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    def __str__(self): return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock_actual = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    def __str__(self): return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=13, unique=True)
    def __str__(self): return self.nombre

class RegistroVenta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    total_pago = models.DecimalField(max_digits=10, decimal_places=2)
