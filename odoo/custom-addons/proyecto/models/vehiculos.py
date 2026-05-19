# -*- coding: utf-8 -*-
from odoo import fields, models


class Vehiculos(models.Model):
    _name = 'empresa.vehiculo'
    _description = 'Tabla de Vechiculos'

    brand = fields.Char(string='Marca')
    model = fields.Char(string= 'Modelo')
    placa = fields.Char(string='Placa')
    