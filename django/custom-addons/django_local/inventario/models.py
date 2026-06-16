from django.db import models


# ─── Modelo existente ───────────────────────────────────────────
class Categoria(models.Model):
    nombre      = models.CharField(max_length=100, unique=True)
    codigo = models.TextField(max_length=5)
    descripcion = models.TextField(blank=True)
    activa      = models.BooleanField(default=True)
    creada_en   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
        return f"({self.codigo}) {self.nombre}"

    class Meta:
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']


# ─── Modelo nuevo 1: para relación N:M ──────────────────────────
class Proveedor(models.Model):
    nombre   = models.CharField(max_length=150)
    contacto = models.EmailField(unique=True)
    pais     = models.CharField(max_length=80, default='Ecuador')

    def __str__(self):
        return self.nombre


# ─── Modelo central: conecta las 3 relaciones ───────────────────
class Producto(models.Model):
    nombre      = models.CharField(max_length=150)
    precio      = models.DecimalField(max_digits=10, decimal_places=2)
    existencias = models.PositiveIntegerField(default=0)

    # 1:N → Categoria
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name='productos'
    )

    # N:M → Proveedor
    proveedores = models.ManyToManyField(
        Proveedor, blank=True, related_name='productos'
    )

    def __str__(self):
        return f"{self.nombre} ({self.categoria.nombre})"


# ─── Modelo nuevo 2: para relación 1:1 ──────────────────────────
class FichaTecnica(models.Model):
    # 1:1 → Producto
    producto = models.OneToOneField(
        Producto, on_delete=models.CASCADE, related_name='ficha_tecnica'
    )
    peso_kg        = models.DecimalField(max_digits=6, decimal_places=2)
    dimensiones    = models.CharField(max_length=50, blank=True)
    garantia_meses = models.PositiveIntegerField(default=12)

    def __str__(self):
        return f"Ficha de {self.producto.nombre}"

