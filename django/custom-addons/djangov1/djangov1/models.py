from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from django.utils import timezone


validar_nombre_persona = RegexValidator(
    regex=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+(?:[ '\-][A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+)*$",
    message=(
        "Use únicamente letras, espacios, apóstrofes o guiones. "
        "No se permiten números ni símbolos especiales."
    ),
)

validar_telefono = RegexValidator(
    regex=r"^\+?[0-9]{7,15}$",
    message=(
        "Ingrese entre 7 y 15 dígitos. Puede comenzar con el signo +, "
        "pero no use espacios ni letras."
    ),
)

validar_sku = RegexValidator(
    regex=r"^[A-Z0-9]+(?:-[A-Z0-9]+)*$",
    message="Use letras mayúsculas, números y guiones, por ejemplo: TEC-001.",
)

validar_codigo_pedido = RegexValidator(
    regex=r"^[A-Z0-9]+(?:-[A-Z0-9]+)*$",
    message="Use letras mayúsculas, números y guiones, por ejemplo: PED-0001.",
)


def calcular_edad(fecha_nacimiento: date, hoy: date | None = None) -> int:
    """Calcula la edad cumplida desde la fecha de nacimiento."""
    hoy = hoy or timezone.localdate()

    return hoy.year - fecha_nacimiento.year - (
        (hoy.month, hoy.day)
        < (fecha_nacimiento.month, fecha_nacimiento.day)
    )


def validar_fecha_nacimiento(fecha_nacimiento: date) -> None:
    """Valida que el cliente tenga entre 18 y 120 años."""
    hoy = timezone.localdate()

    if fecha_nacimiento > hoy:
        raise ValidationError(
            "La fecha de nacimiento no puede estar en el futuro."
        )

    edad = calcular_edad(fecha_nacimiento, hoy)

    if edad < 18:
        raise ValidationError(
            "El cliente debe tener al menos 18 años."
        )

    if edad > 120:
        raise ValidationError(
            "La edad no puede ser mayor a 120 años."
        )


class Categoria(models.Model):
    nombre = models.CharField(
        max_length=100,
        unique=True,
        validators=[MinLengthValidator(2)],
    )
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    slug = models.SlugField(max_length=120, unique=True)
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "categoría"
        verbose_name_plural = "categorías"

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(2)],
    )
    correo = models.EmailField(unique=True)
    telefono = models.CharField(
        max_length=16,
        validators=[validar_telefono],
    )
    sitio_web = models.URLField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "proveedor"
        verbose_name_plural = "proveedores"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(2)],
    )
    sku = models.CharField(
        "SKU",
        max_length=30,
        unique=True,
        validators=[validar_sku],
        help_text="Formato recomendado: TEC-001.",
    )
    descripcion = models.TextField(blank=True)

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="productos",
    )

    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name="productos",
    )

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    stock = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=5)
    disponible = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=170, unique=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "producto"
        verbose_name_plural = "productos"

    @property
    def necesita_reposicion(self):
        return self.stock <= self.stock_minimo

    def __str__(self):
        return f"{self.nombre} ({self.sku})"


class Cliente(models.Model):
    nombres = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2),
            validar_nombre_persona,
        ],
        help_text=(
            "Solo letras; se permiten espacios, apóstrofes y guiones."
        ),
    )

    apellidos = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2),
            validar_nombre_persona,
        ],
        help_text=(
            "Solo letras; se permiten espacios, apóstrofes y guiones."
        ),
    )

    correo = models.EmailField(unique=True)

    telefono = models.CharField(
        max_length=16,
        blank=True,
        validators=[validar_telefono],
        help_text="Ejemplo: 0991234567 o +593991234567.",
    )

    direccion = models.TextField(
        validators=[MinLengthValidator(5)]
    )

    fecha_nacimiento = models.DateField(
        null=True,
        blank=False,
        validators=[validar_fecha_nacimiento],
        help_text=(
            "Debe corresponder a una persona de 18 a 120 años."
        ),
    )

    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["apellidos", "nombres"]
        verbose_name = "cliente"
        verbose_name_plural = "clientes"

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}".strip()

    @property
    def edad(self):
        if not self.fecha_nacimiento:
            return None

        return calcular_edad(self.fecha_nacimiento)

    def __str__(self):
        return self.nombre_completo


class Pedido(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        PAGADO = "pagado", "Pagado"
        ENVIADO = "enviado", "Enviado"
        ENTREGADO = "entregado", "Entregado"
        CANCELADO = "cancelado", "Cancelado"

    codigo = models.CharField(
        max_length=20,
        unique=True,
        validators=[validar_codigo_pedido],
        help_text="Formato recomendado: PED-0001.",
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="pedidos",
    )

    productos = models.ManyToManyField(
        Producto,
        through="DetallePedido",
        related_name="pedidos",
    )

    fecha = models.DateTimeField(auto_now_add=True)

    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )

    observaciones = models.TextField(blank=True)
    entregado = models.BooleanField(default=False)

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "pedido"
        verbose_name_plural = "pedidos"

    @property
    def total(self):
        return sum(
            (
                detalle.subtotal
                for detalle in self.detalles.all()
            ),
            Decimal("0.00"),
        )

    def __str__(self):
        return f"Pedido {self.codigo} - {self.cliente}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="detalles",
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name="detalles_pedido",
    )

    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )

    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.01")),
        ],
        help_text=(
            "Precio utilizado en la venta. "
            "Se copia automáticamente desde el producto."
        ),
    )

    descuento = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        help_text="Porcentaje de descuento entre 0 y 100.",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "pedido",
                    "producto",
                ],
                name="detalle_unico_por_producto_y_pedido",
            )
        ]

        ordering = [
            "pedido",
            "producto",
        ]

        verbose_name = "detalle de pedido"
        verbose_name_plural = "detalles de pedido"

    def clean(self):
        errores = {}

        if self.producto_id and self.cantidad:
            if self.cantidad > self.producto.stock:
                errores["cantidad"] = (
                    f"Stock insuficiente. El producto tiene "
                    f"{self.producto.stock} unidades disponibles."
                )

        if errores:
            raise ValidationError(errores)

    def save(self, *args, **kwargs):
        """
        Si no se proporciona precio, copia el precio actual del producto.

        El precio queda guardado en el detalle para que los pedidos
        históricos no cambien cuando cambie el precio del producto.
        """

        if self.producto_id and self.precio_unitario is None:
            self.precio_unitario = self.producto.precio

        super().save(*args, **kwargs)

    @property
    def subtotal_sin_descuento(self):
        return (
            self.precio_unitario * self.cantidad
        ).quantize(Decimal("0.01"))

    @property
    def valor_descuento(self):
        porcentaje = (
            self.descuento / Decimal("100.00")
        )

        return (
            self.subtotal_sin_descuento * porcentaje
        ).quantize(Decimal("0.01"))

    @property
    def subtotal(self):
        return (
            self.subtotal_sin_descuento
            - self.valor_descuento
        ).quantize(Decimal("0.01"))

    def __str__(self):
        return (
            f"{self.pedido.codigo}: "
            f"{self.producto.nombre} x {self.cantidad}"
        )

