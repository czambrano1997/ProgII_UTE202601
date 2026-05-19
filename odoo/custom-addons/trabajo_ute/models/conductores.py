# -*- coding: utf-8 -*-
from odoo import fields, models


class Conductores(models.Model):
    _name = 'ou.conductores'

    name = fields.Char(string='Conductores')

    name = fields.Char(string="Ingrese Nombre", required=True)
    last_name = fields.Char(string="Ingrese Apellido", required=True)
    email=fields.Char(string="Correo")
    phone= fields.Char(string="Teléfono")
    vat = fields.Char(string="CI/RUC", size=13)