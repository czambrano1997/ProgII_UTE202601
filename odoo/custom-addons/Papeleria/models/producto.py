# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductoPapeleria(models.Model):
    """
    Extendemos product.template para agregar campos específicos
    de papelería: stock mínimo y categoría interna.
    El precio ya existe en product.template (list_price).
    """
    _inherit = 'product.template'

    # Campo para marcar que el producto pertenece a la papelería
    es_producto_papeleria = fields.Boolean(
        string='Es producto de papelería',
        default=False,
    )

    stock_minimo = fields.Float(
        string='Stock Mínimo',
        default=0.0,
        help='Cantidad mínima antes de generar alerta de reabastecimiento',
    )

    # Nota: la categoría usa product.category (campo categ_id heredado)
    # No es necesario redefinirlo, solo se usa en las vistas.
    # Nota: list_price (Precio de Venta) ya existe en product.template

    @api.constrains('stock_minimo')
    def _check_stock_minimo(self):
        for rec in self:
            if rec.stock_minimo < 0:
                raise ValidationError("El stock mínimo no puede ser negativo.")
