from django.db import models

# Create your models 
class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    edad =models.IntegerField()

class Cartegoria(models.Model):
    nombre = models.CharField(max_length=100)

class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    fecha_publicacion = models.DateField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)

    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    castegoria = models.ForeignKey(Cartegoria, on_delete=models.CASCADE)

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()


class Prestamo(models.Model):
    fecha_prestamo = models.DateField()
    fecha_devolucon = models.DateField()

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro,on_delete=models.CASCADE)
