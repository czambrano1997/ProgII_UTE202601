# -*- coding: utf-8 -*-
from odoo import models, fields, api


class TeatroBoleto(models.Model):
    _name = 'teatro.boleto'
    _description = 'Boleto de teatro'
    _rec_name = 'name'
    _order = 'fecha_compra desc, name'

    name = fields.Char(
        string='Número',
        required=True,
        copy=False,
        default='Nuevo',
    )
    funcion_id = fields.Many2one(
        comodel_name='teatro.funcion',
        string='Función',
        required=True,
        ondelete='cascade',
    )
    cliente = fields.Char(string='Cliente')
    asiento = fields.Char(string='Asiento')
    precio = fields.Monetary(
        string='Precio',
        required=True,
        default=0.0,
        currency_field='currency_id',
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id,
        required=True,
    )
    estado = fields.Selection(
        [
            ('reservado', 'Reservado'),
            ('pagado', 'Pagado'),
            ('anulado', 'Anulado'),
        ],
        string='Estado',
        default='reservado',
        required=True,
    )
    fecha_compra = fields.Date(
        string='Fecha de compra',
        default=fields.Date.context_today,
    )

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('teatro.boleto') or 'Nuevo'
        return super().create(vals)
