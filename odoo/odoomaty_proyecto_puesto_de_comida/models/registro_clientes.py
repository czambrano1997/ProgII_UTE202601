# -*- coding: utf-8 -*-
from odoo import fields, models

class ComidaCliente(models.Model):
    _name = 'comida.cliente'
    _description = 'Clientes del Puesto'

    name = fields.Char(string="Nombre del Cliente", required=True)
    telefono = fields.Char(string="Número de Teléfono")
    email = fields.Char(string="Correo Electrónico")