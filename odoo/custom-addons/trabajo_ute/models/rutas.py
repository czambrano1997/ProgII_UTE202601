# -*- coding: utf-8 -*-
from odoo import fields, models


class Rutas(models.Model):
    _name = 'ou.rutas'

    name = fields.Char(string='Ruta')
