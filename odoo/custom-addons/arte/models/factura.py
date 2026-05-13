# -*- coding: utf-8 -*-
from odoo import fields, models


class Factura(models.Model):
    _name = 'factura'

    nombre = fields.Char(string='Name')
    pedido_id = fields.Many2one(
        'arte.pedido',
        string='pedido',
        
        )
    cliente = fields.Char(related='pedido_id.cliente')
    correo = fields.Char(related='pedido_id.correo')
    telefono = fields.Char(related='pedido_id.telefono')
