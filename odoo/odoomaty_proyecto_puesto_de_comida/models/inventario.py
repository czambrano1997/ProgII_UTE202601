# -*- coding: utf-8 -*-
from odoo import fields, models

class ComidaIngrediente(models.Model):
    _name = 'comida.ingrediente'
    _description = 'Materia prima / Ingredientes'

    name = fields.Char(string="Nombre del Ingrediente", required=True)
    stock = fields.Integer(string="Cantidad en Bodega", default=10)