# -*- coding: utf-8 -*-
from odoo import fields, models


class Producto(models.Model):
    _name = 'empresa.producto'
    _description = 'Tabla de Productos'
    name = fields.Char(string='Producto')
    price = fields.Float(string='Precio')
    stock = fields.Integer(string='Stock')
    
