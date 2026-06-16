from django.db import models

class TipoFlor(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()

    def __str__(self):
        return self.nombre
    

class Flor(models.Model):
    nombre = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=8,decimal_places=2)
    stock = models.IntegerField()
    fecha_ingreso = models.DateField()

    tipo = models.ForeignKey(TipoFlor, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str_(self):
        return self.nombre
    

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre
    

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    flor = models.ForeignKey(Flor,on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id}"
        

