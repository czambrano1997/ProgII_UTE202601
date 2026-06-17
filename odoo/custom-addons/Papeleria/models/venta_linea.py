# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class VentaLinea(models.Model):
    """
    Líneas de detalle de una venta en la papelería.
    Cada línea referencia un producto, cantidad y precio unitario.
    El subtotal se calcula automáticamente con @api.depends.
    """
    _name = 'papeleria.venta.linea'
    _description = 'Línea de Venta Papelería'

    venta_id = fields.Many2one(
        comodel_name='papeleria.venta',
        string='Venta',
        required=True,
        ondelete='cascade',
    )

    producto_id = fields.Many2one(
        comodel_name='product.product',
        string='Producto',
        required=True,
    )

    cantidad = fields.Float(
        string='Cantidad',
        default=1.0,
        required=True,
    )

    precio_unitario = fields.Float(
        string='Precio Unitario',
        digits='Product Price',
    )

    subtotal = fields.Float(
        string='Subtotal',
        compute='_compute_subtotal',
        store=True,
    )

    # ─── Compute: subtotal ────────────────────────────────────────────────────

    @api.depends('cantidad', 'precio_unitario')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.cantidad * rec.precio_unitario

    # ─── Onchange: autocompletar precio al seleccionar producto ──────────────

    @api.onchange('producto_id')
    def _onchange_producto_id(self):
        """
        Al seleccionar el producto, se autocompleta el precio unitario
        con el precio de lista (list_price) del product.template.
        """
        if self.producto_id:
            self.precio_unitario = self.producto_id.lst_price

    # ─── Constraint: validar stock disponible ────────────────────────────────

    @api.constrains('cantidad', 'producto_id')
    def _check_stock_disponible(self):
        """
        Valida que la cantidad solicitada no supere el stock disponible
        usando product.qty_available (campo de odoo/stock).
        """
        for rec in self:
            if not rec.producto_id:
                continue
            stock = rec.producto_id.qty_available
            if rec.cantidad > stock:
                raise ValidationError(
                    f"No hay suficiente stock para '{rec.producto_id.name}'.\n"
                    f"Stock disponible: {stock} | Cantidad solicitada: {rec.cantidad}"
                )

    # ─── Constraint: cantidad positiva ───────────────────────────────────────

    @api.constrains('cantidad')
    def _check_cantidad(self):
        for rec in self:
            if rec.cantidad <= 0:
                raise ValidationError("La cantidad debe ser mayor a 0.")
