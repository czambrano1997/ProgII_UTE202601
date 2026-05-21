# -*- coding: utf-8 -*-
from odoo import fields, models


class Pedido(models.Model):
    _name = 'arte.pedido'


    name = fields.Char(string='Nombre pedido')
    cliente = fields.Char(string="Cliente", required=False, tracking=True, translate=True)
    celuda =fields.Char(string="celuda", required=False, tracking=True,size=10  )
    correo = fields.Char(string="correo" , required=False ,  tracking=True, translate=True)
    telefono = fields.Char(string="telefono", required=False, tracking=True, size=11)
    precio=fields.Float(string="precio", digits=(16, 2), tracking=True)
    direccion = fields.Char(string="direccion", required=False, tracking=True, translate=True)
    
    