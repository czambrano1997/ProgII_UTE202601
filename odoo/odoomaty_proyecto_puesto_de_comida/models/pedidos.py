# -*- coding: utf-8 -*-
from odoo import fields, models


class Pedidos(models.Model):
    _name = 'pedidos'

    name = fields.Char(string='Name')
