from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Producto(models.Model):
    _name = 'choco.producto'
    _description = 'Productos'

    nombre = fields.Char(string='Nombre', required=True)
    precio = fields.Float(string='Precio')
    stock = fields.Integer(string='Stock')
    tipo = fields.Selection([
        ('negro', 'Chocolate Negro'),
        ('leche', 'Chocolate de Leche'),
        ('blanco', 'Chocolate Blanco')
    ], string='Tipo')

    disponible = fields.Boolean(string='Disponible', default=True)

    @api.constrains('stock')
    def _check_stock(self):
        for record in self:
            if record.stock < 0:
                raise ValidationError("El stock no puede ser negativo")