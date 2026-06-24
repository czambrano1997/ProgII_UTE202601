from django.db import models

# Create your models here.

class Producto (models.Model):
    nombre = models.CharField(
        max_length=100)
    precio = models.DecimalField(
        max_digits=8,
        decimal_places=2)
    stock = models.IntegerField(
        default=0)
    
def __str__(self):
    return self.nombre
