# -*- coding: utf-8 -*-
from odoo import fields, models


class Pedido(models.Model):
    _name = 'arte.pedido'


    name = fields.Char(string='Nombre pedido')
    cliente = fields.Char(string="Cliente", required=False, tracking=True, translate=True)
    celuda =fields.Char(string="celuda", required=False, tracking=True,size=10  )
    correo = fields.Char(string="correo" , required=False ,  tracking=True, translate=True)
    telefono = fields.Char(string="telefono", required=False, tracking=True, size=11)
    direcion = fields.Char(string="direccion", required=False, tracking=True, translate=True)
    precio= fields.Char(string="precio", required=False,tracking=True, size=4)


    state = fields.Selection([
        ('pediente', 'Pediente'),
        ('en_progreso', 'En Progreso'),
        ('cancelo', 'Cancelo'),
        ("confirmando","Confirmando")
    ], string='Status', default='pediente', tracking=True)

    def confirma(self):
        self.state = "confirmando"
    