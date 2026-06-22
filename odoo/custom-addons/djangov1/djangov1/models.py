from django.db import models


class Obra(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    duracion_min = models.IntegerField()
    fecha_estreno = models.DateField()

    class Meta:
        ordering = ['titulo']
        verbose_name_plural = 'Obras'

    def __str__(self):
        return self.titulo


class Actor(models.Model):
    nombre = models.CharField(max_length=150)
    edad = models.IntegerField()
    nacionalidad = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = 'Actores'

    def __str__(self):
        return self.nombre


class Funcion(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='funciones')
    fecha = models.DateTimeField()
    sala = models.CharField(max_length=100)
    entradas_disponibles = models.IntegerField()

    class Meta:
        ordering = ['fecha']
        verbose_name_plural = 'Funciones'

    def __str__(self):
        return f"{self.obra.titulo} - {self.fecha}"


class Participacion(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='participaciones')
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='participaciones')
    personaje = models.CharField(max_length=150)

    class Meta:
        ordering = ['obra', 'actor']
        verbose_name_plural = 'Participaciones'

    def __str__(self):
        return f"{self.actor.nombre} en {self.obra.titulo}"


class Boleto(models.Model):
    funcion = models.ForeignKey(Funcion, on_delete=models.CASCADE, related_name='boletos')
    cliente_nombre = models.CharField(max_length=150)
    cliente_email = models.EmailField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    asiento = models.CharField(max_length=20)
    fecha_compra = models.DateField()
    confirmado = models.BooleanField(default=True)

    class Meta:
        ordering = ['-fecha_compra']
        verbose_name_plural = 'Boletos'

    def __str__(self):
        return f'Boleto {self.asiento} para {self.funcion}'
