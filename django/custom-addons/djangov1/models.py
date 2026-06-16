from django.db import models


class Autor(models.Model):
    nombre = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    web = models.URLField(blank=True)
    biografia = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class CategoriaLibro(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    titulo = models.CharField(max_length=220)
    subtitulo = models.CharField(max_length=220, blank=True)
    isbn = models.CharField(max_length=20, unique=True)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    paginas = models.PositiveIntegerField()
    disponible = models.BooleanField(default=True)
    fecha_publicacion = models.DateField()
    categoria = models.ForeignKey(CategoriaLibro, on_delete=models.CASCADE, related_name='libros')
    autores = models.ManyToManyField(Autor, related_name='libros', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class Cliente(models.Model):
    nombre = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    direccion = models.TextField(blank=True)
    fecha_registro = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Prestamo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='prestamos')
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='prestamos')
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField(blank=True, null=True)
    devuelto = models.BooleanField(default=False)
    multa = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    observaciones = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Préstamo {self.id} - {self.libro.titulo}"
