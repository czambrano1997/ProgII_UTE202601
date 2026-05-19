# -*- coding: utf-8 -*-
from odoo import fields, models


class Pedidos(models.Model):
    _name = 'empresa.pedidos'
    _description = 'Tabla de Pedidos'
    client = fields.Char(string='CLiente')
    date = fields.Date(string='Fecha')
    total = fields.float(string='Total')