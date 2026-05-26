# -*- coding: utf-8 -*-
from odoo import fields, models


class Menu(models.Model):
    _name = 'menu'

    name = fields.Char(string='Name')
