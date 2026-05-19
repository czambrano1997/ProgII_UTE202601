# -*- coding: utf-8 -*-
from odoo import fields, models


class Empleados(models.Model):
    _name = 'empresa.empleados'
    _description ='Tabla de Empleados '

    name = fields.Char(string='Nombre')
    charge = fields.Char(string='Cargo')
    salary = fields.Float(string='Salario')
