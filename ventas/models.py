from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Producto(models.Model):
    CATEGORIA_CHOICES = [
        ('PAN', 'Panadería'),
        ('PAS', 'Pastelería'),
        ('GAL', 'Galletería'),
        ('POS', 'Postres'), 
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True) 
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    categoria = models.CharField(
        max_length=3, 
        choices=CATEGORIA_CHOICES, 
        default='PAN'
    )
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    disponible = models.BooleanField(default=True, verbose_name="¿Disponible para la venta?")

    # --- AUMENTO 1: Lógica de protección de Stock ---
    def save(self, *args, **kwargs):
        # Si el stock es 0 o menos, el producto se oculta solo
        if self.stock <= 0:
            self.stock = 0
            self.disponible = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.get_categoria_display()}) - Stock: {self.stock}"

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Entregado', 'Entregado'),
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Cliente")
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name="Teléfono de contacto")
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    completado = models.BooleanField(default=False, verbose_name="¿Venta Finalizada?")
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='Pendiente'
    )

    # --- AUMENTO 2: Ordenar por fecha (lo más nuevo arriba) ---
    class Meta:
        ordering = ['-fecha_pedido']

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.username} ({self.estado})"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return Decimal(str(self.cantidad)) * Decimal(str(self.precio_unitario))

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"