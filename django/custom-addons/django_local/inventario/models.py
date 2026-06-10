from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=5, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        # ordering = ['codigo']
        return f"{self.codigo} - {self.nombre}"
