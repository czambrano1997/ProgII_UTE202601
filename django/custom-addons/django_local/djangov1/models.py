from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    activa = models.BooleanField(default=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    empresa = models.CharField(max_length=100)
    email_contacto = models.EmailField()
    sitio_web = models.URLField(blank=True, null=True)
    fecha_asociacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.empresa

class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, related_name='productos')
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    identificacion = models.CharField(max_length=20, unique=True)
    nombre_completo = models.CharField(max_length=150)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    es_vip = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_completo

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='ventas')
    productos = models.ManyToManyField(Producto, related_name='ventas')
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Venta {self.id} - {self.cliente}"
    
class Cantidad_producto (models.Model):
    cantidad= models.CharField(max_length=15, unique=True)
    