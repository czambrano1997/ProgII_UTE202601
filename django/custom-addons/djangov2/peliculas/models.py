from django.db import models

# Create your models here.


class Pelicula(models.Model):

    titulo = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)
    fecha_estreno = models.DateField()
    duracion = models.IntegerField()
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo
    
class Sala(models.Model):
    nombre = models.CharField(max_length=50)
    capacidad = models.IntegerField()

    def __str__(self):
        return self.nombre


class Funcion(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    precio = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.pelicula} - {self.fecha}"


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()

    def __str__(self):
        return self.nombre


class Boleto(models.Model):
    funcion = models.ForeignKey(Funcion, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    asiento = models.CharField(max_length=5)
    pagado = models.BooleanField(default=False)

    def __str__(self):
        return f"Boleto {self.id} de {self.cliente}"

