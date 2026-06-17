# -*- coding: utf-8 -*-
from odoo import models, fields


class ProveedorPapeleria(models.Model):
   
    _inherit = 'res.partner'

    es_proveedor_papeleria = fields.Boolean(
        string='Es proveedor de papelería',
        default=False,
    )

    ruc = fields.Char(
        string='RUC / Identificación',
        size=13,
    )

    plazo_entrega = fields.Integer(
        string='Plazo de entrega (días)',
        default=1,
        help='Días promedio que tarda el proveedor en entregar los pedidos',
    )

    # Nota: es_cliente_papeleria y es_proveedor_papeleria no se
    # excluyen mutuamente; un partner puede ser ambas cosas.
