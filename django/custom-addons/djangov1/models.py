from django.db import models

# Create your models here.
class clientes(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    fecha_registro = models.DecimalField(auto_created=True)