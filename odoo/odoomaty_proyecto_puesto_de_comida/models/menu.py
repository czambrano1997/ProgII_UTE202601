# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo import ValidationError

class ComidaPlatillo(models.Model):
    _name = 'comida.platillo'
    _description = 'Platillos de Comida'

    name = fields.Char(string="Nombre del Platillo", required=True)
    precio = fields.Float(string="Precio Público", required=True)
    categoria = fields.Selection([
        ('hamburguesa', 'Hamburguesas'),
        ('bebida', 'Bebidas'),
        ('snack', 'Papas/Snacks')
    ], string="Categoría", default='hamburguesa')
    disponible = fields.Boolean(string="Disponible para Venta", default=True)
    ingrediente_ids = fields.Many2many('comida.ingrediente', string="Ingredientes Usados")
    @api.constrains('precio')
    def _check_precio_positivo(self):
        for record in self:
            if record.precio <= 0:
                raise ValidationError("El precio del platillo debe ser mayor a $0.00.")