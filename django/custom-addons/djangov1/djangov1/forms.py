from django import forms
from django.core.exceptions import ValidationError

from .models import DetallePedido


class DetallePedidoAdminForm(forms.ModelForm):
    """
    Formulario usado por Django Admin para los detalles de pedido.

    El precio unitario puede dejarse vacío. En ese caso se toma
    automáticamente el precio actual registrado en el producto.
    """

    class Meta:
        model = DetallePedido
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["precio_unitario"].required = False

        self.fields["precio_unitario"].help_text = (
            "Se completa automáticamente con el precio actual "
            "del producto. Puede modificarse para una venta especial."
        )

        self.fields["cantidad"].help_text = (
            "La cantidad no puede superar el stock disponible."
        )

    def clean(self):
        datos = super().clean()

        producto = datos.get("producto")
        cantidad = datos.get("cantidad")
        precio_unitario = datos.get("precio_unitario")

        if producto and precio_unitario is None:
            datos["precio_unitario"] = producto.precio

        if producto and cantidad:
            if cantidad > producto.stock:
                self.add_error(
                    "cantidad",
                    (
                        f"Stock insuficiente. Actualmente existen "
                        f"{producto.stock} unidades disponibles."
                    ),
                )

        return datos