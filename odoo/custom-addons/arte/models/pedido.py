# -*- coding: utf-8 -*-
from odoo import fields, models


class Pedido(models.Model):
    _name = 'arte.pedido'


    name = fields.Char(string='Nombre pedido')
    cliente = fields.Char(string="Cliente", required=False, tracking=True, translate=True)
    correo = fields.Char(string="correo" , required=False ,  tracking=True, translate=True)
    telefono = fields.Char(string="telefono", required=False, tracking=True, size=11)
    