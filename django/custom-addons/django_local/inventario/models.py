from django.db import models

# Create your models here.
class Genero(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        # ordering = ['codigo']
        return f"{self.codigo} - {self.nombre}"
    

class Artista(models.Model):
    nombre = models.CharField(max_length=20)
    pais = models.CharField(max_length= 50)

    def __str__(self):
        return self.nombre
    

class Disco(models.Model):
    titulo = models.CharField(max_length= 50)
    precio = models.CharField(max_length=100)
    stock = models.IntegerField()

    genero = models.ForeignKey(
        Genero,
        on_delete=models.CASCADE
    )

    artista = models.ForeignKey(
        Artista,
        on_delete=models.CASCADE
    )
  
    def __str__(self):
        return self.titulo


class Cliente (models.Model):
    nombre = models.CharField(max_length = 80)
    correo = models.CharField(max_length=70)
    telefono = models.IntegerField()

    def __str__(self):
        return self.nombre
    
class Venta(models.Model):
    fecha = models.DateField()

    disco = models.ForeignKey(
        Disco,
        on_delete = models.CASCADE
        
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete = models.CASCADE
    )

    cantidad = models.IntegerField()
    def __str__(self):
        return f"Venta {self.id}"
    

    