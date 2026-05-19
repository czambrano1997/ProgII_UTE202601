from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Detalle(models.Model):
    _name = 'choco.detalle'
    _description = 'Detalle Pedido'

    pedido_id = fields.Many2one(
        'choco.pedido',
        string='Pedido'
    )

    producto_id = fields.Many2one(
        'choco.producto',
        string='Producto'
    )

    cantidad = fields.Integer(string='Cantidad')

    precio = fields.Float(string='Precio')

    subtotal = fields.Float(
        string='Subtotal',
        compute='_compute_subtotal',
        store=True
    )

    @api.onchange('producto_id')
    def _onchange_producto(self):
        if self.producto_id:
            self.precio = self.producto_id.precio

    @api.depends('cantidad', 'precio')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.cantidad * record.precio

    @api.constrains('cantidad')
    def _check_cantidad(self):
        for record in self:
            if record.cantidad <= 0:
                raise ValidationError(
                    "La cantidad debe ser mayor a cero"
                )