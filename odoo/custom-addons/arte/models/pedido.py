# -*- coding: utf-8 -*-
from odoo import fields, models


class Pedido(models.Model):
    _name = 'arte.pedido'


    name = fields.Char(string='Nombre pedido')
    cliente=fields.Char(string="Cliente", required=False, tracking=True, translate=True)
