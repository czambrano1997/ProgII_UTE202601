from django.db import models

# Modelo Clientes
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    s_nombre = models.CharField(max_length=100, blank=True, verbose_name='Segundo nombre')
    apellido = models.CharField(max_length=100)
    s_apellido = models.CharField(max_length=100, blank=True, verbose_name='Segundo apellido')
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, verbose_name="Telefono")
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


# Modelo paquete
class Paquete(models.Model):
    nombre_p = models.CharField(max_length=100)
    costo_p = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo del paquete")
    descripcion = models.TextField(verbose_name="Descripcion del paquete")

    def __str__(self):
        return self.nombre_p


# Modelo Reservas
class Reserva(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    numero_Rs = models.AutoField(primary_key=True)
    Hora_ll = models.TimeField(auto_now=False, auto_now_add=False, null=False, blank=False, verbose_name="Hora de llegada")
    Hora_Sa = models.TimeField(auto_now=False, auto_now_add=False, null=False, blank=False, verbose_name="Hora de salida")
    Pago = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_ju = models.IntegerField(verbose_name="Numero de jugadores")
    paquete_incluido = models.ForeignKey('Paquete', on_delete=models.CASCADE, null=True, blank=True)
    nota = models.TextField(verbose_name="Nota extra de la reservacion")

    def __str__(self):
        return f"{self.cliente} {self.numero_Rs}"


# Modelo inventario
class Inventario(models.Model):
    nombre_p = models.CharField(max_length=100, null=True, blank=True,verbose_name='Producto')
    precio_p = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio unitario")
    cantidad_p = models.IntegerField(verbose_name="Cantidad del producto", null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_p}-{self.cantidad_p}"


# Modelo gestion de reservas
class Gestion_reserva(models.Model):
    nombre_cli = models.OneToOneField('Cliente', on_delete=models.CASCADE)
    canchas = models.ForeignKey('Reserva', on_delete=models.CASCADE)
    reservo = models.BooleanField(default=False, verbose_name="Si llego")
    productos_de_consumo = models.ManyToManyField('Inventario', through='DetalleConsumo', verbose_name="Productos consumidos")

    def __str__(self):
        return f"{self.nombre_cli} - {self.reservo}"
    
class DetalleConsumo(models.Model):
    gestion = models.ForeignKey('Gestion_reserva', on_delete=models.CASCADE)
    producto = models.ForeignKey('Inventario', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad")

    def __str__(self):
        return f"{self.cantidad} x {self.producto}"