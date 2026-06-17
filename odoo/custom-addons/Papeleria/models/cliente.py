# -*- coding: utf-8 -*-
from odoo import models, fields


class ClientePapeleria(models.Model):
    """
    Extendemos res.partner para identificar clientes de la papelería.
    Odoo ya distingue customer_rank y supplier_rank en res.partner,
    pero agregamos un campo explícito para filtrado interno.
    """
    _inherit = 'res.partner'

    es_cliente_papeleria = fields.Boolean(
        string='Es cliente de papelería',
        default=False,
    )

    # Campo de relación inversa: todas las ventas de este cliente
    venta_ids = fields.One2many(
        comodel_name='papeleria.venta',
        inverse_name='cliente_id',
        string='Ventas',
    )

    total_compras = fields.Float(
        string='Total compras',
        compute='_compute_total_compras',
        store=False,
    )

    def _compute_total_compras(self):
        for rec in self:
            rec.total_compras = sum(rec.venta_ids.mapped('total'))
