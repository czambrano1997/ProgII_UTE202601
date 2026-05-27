# -*- coding: utf-8 -*-
from odoo import fields, models,api


class OdoomatyProyectoPuestoDeComida(models.Model):
    _name = 'odoomaty.proyecto.puesto.de.comida'
    _description = 'Pedidos del Puesto de Comida'
    name = fields.Char(string="Código de Pedido", required=True, default="Nuevo")
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado'),
        ('done', 'Entregado')
    ], default='draft', string="Estado")
    description = fields.Text(string="Notas del Pedido")
    amount = fields.Float(string="Total a Pagar", compute="_compute_amount_total", store=True)
    active = fields.Boolean(default=True, string="Activo")
    fecha = fields.Date(string="Fecha", default=fields.Date.today)
    
    cliente_id = fields.Many2one('comida.cliente', string="Cliente")
    linea_ids = fields.One2many('comida.pedido.linea', 'pedido_id', string="Líneas de Comida")

    @api.depends('linea_ids.subtotal')
    def _compute_amount_total(self):
        for pedido in self:
            pedido.amount = sum(linea.subtotal for linea in pedido.linea_ids)