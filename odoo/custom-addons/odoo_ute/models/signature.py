# -*- coding: utf-8 -*-
from odoo import fields, models


class Signature(models.Model):
    _name = 'ou.signature'
    _description = 'Firma'

    name = fields.Char(string='Materia')
