from django.db import models


class Autor(models.Model):
    nombre = models.CharField(max_length=120)
    apellido = models.CharField(max_length=120)
    email = models.EmailField(blank=True, null=True)
    biografia = models.TextField(blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['apellido', 'nombre']
        verbose_name_plural = 'Autores'

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


class Editorial(models.Model):
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=250, blank=True)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True)
    pagina_web = models.URLField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = 'Editoriales'

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    sinopsis = models.TextField(blank=True)
    isbn = models.CharField(max_length=20, blank=True)
    paginas = models.IntegerField(default=0)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    disponible = models.BooleanField(default=True)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE, related_name='libros')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='libros')

    class Meta:
        ordering = ['titulo']
        verbose_name_plural = 'Libros'

    def __str__(self):
        return self.titulo


class Prestamo(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='prestamos')
    usuario_nombre = models.CharField(max_length=140)
    usuario_email = models.EmailField()
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField(blank=True, null=True)
    devuelto = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha_prestamo']
        verbose_name_plural = 'Préstamos'

    def __str__(self):
        return f'Préstamo de {self.libro} a {self.usuario_nombre}'
