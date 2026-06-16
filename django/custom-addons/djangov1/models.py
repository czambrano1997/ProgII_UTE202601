from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    sku = models.CharField(max_length=20, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos')
    proveedores = models.ManyToManyField(Proveedor, blank=True, related_name='productos')
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.sku} - {self.nombre}"


class Almacen(models.Model):
    nombre = models.CharField(max_length=120)
    direccion = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.nombre


class EntradaStock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='entradas')
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, related_name='entradas')
    cantidad = models.IntegerField()
    fecha = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.producto} @ {self.almacen}: {self.cantidad}"
