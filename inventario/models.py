from django.db import models


# Modelo Producto
class Producto(models.Model):
	nombre = models.CharField(max_length=200)
	precio = models.DecimalField(max_digits=10, decimal_places=2)
	existencia = models.IntegerField(default=0)
	creado = models.DateTimeField(auto_now_add=True)
	actualizado = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["nombre"]

	def __str__(self):
		return self.nombre


# Modelo Categoria
class Categoria(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
