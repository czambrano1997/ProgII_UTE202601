# -*- coding: utf-8 -*-
from odoo import fields, models


class RegistroClientes(models.Model):
    _name = 'registro.clientes'

    name = fields.Char(string='Name')
