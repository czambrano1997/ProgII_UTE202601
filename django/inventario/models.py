from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=5, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"