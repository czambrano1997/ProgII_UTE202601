from django.db import models

# Create your models here.

class Producto(models.Model):
    nombre= models.CharField(max_length=100)
    codigo=models.CharField(max_length=100)
    descripcion= models.TextField(blank=True)


    def __str__(self):
        ordering= ['codigo']
        return f"{self.codigo}-{self.nombre}"

