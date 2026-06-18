from django.db import models

<<<<<<< HEAD

# Proveedor
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    ruc = models.CharField(max_length=13, unique=True)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

# Categoria
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

# Producto relacion con rpoveedor y categoria
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

# Cliente
class Cliente(models.Model):
    nombre_completo = models.CharField(max_length=150)
    cedula = models.CharField(max_length=10, unique=True)
    correo = models.EmailField()

    def __str__(self):
        return self.nombre_completo

# Pedido relacon con cliente y rpoducto)
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.nombre_completo}"
=======
# Create your models here.
>>>>>>> refs/remotes/origin/estudiante/gomez_danny
