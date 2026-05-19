# -*- coding: utf-8 -*-
from odoo import fields, models


class Cliente(models.Model):
    _name = 'empresa.cliente'
    _description = 'Tabla de Clientes'

    name = fields.Char(string='Nombre')
    vat = fields.Char(string="CI/RUC", size=13)
    email = fields.Char(string="Correo")
    phone = fields.Char(string="Teléfono")
    direction = fields.Char(string="Dirección")
    validate_email = fields.Char(string="Validación", compute='_compute_validate_email',)

cliente_id = fields.Many2one(
    'empresa.cliente',
    string='Cliente')
    