# -*- coding: utf-8 -*-
from odoo import fields, models


class Inventario(models.Model):
    _name = 'inventario'

    name = fields.Char(string='Name')
