# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Venta(models.Model):
    """
    Modelo principal de ventas de la papelería.
    Relaciona un cliente, una fecha, y las líneas de detalle.
    El total se computa sumando los subtotales de cada línea.
    """
    _name = 'papeleria.venta'
    _description = 'Venta Papelería'
    _order = 'fecha desc'

    name = fields.Char(
        string='Referencia',
        required=True,
        default='Nueva Venta',
        copy=False,
    )

    cliente_id = fields.Many2one(
        comodel_name='res.partner',
        string='Cliente',
        required=True,
        domain=[('es_cliente_papeleria', '=', True)],
    )

    fecha = fields.Date(
        string='Fecha',
        required=True,
        default=fields.Date.today,
    )

    state = fields.Selection(
        string='Estado',
        selection=[
            ('borrador', 'Borrador'),
            ('confirmada', 'Confirmada'),
            ('cancelada', 'Cancelada'),
        ],
        default='borrador',
        required=True,
    )

    lineas_venta = fields.One2many(
        comodel_name='papeleria.venta.linea',
        inverse_name='venta_id',
        string='Líneas de Venta',
    )

    total = fields.Float(
        string='Total',
        compute='_compute_total',
        store=True,
    )

    notas = fields.Text(string='Notas internas')

    # ─── Compute: total ──────────────────────────────────────────────────────

    @api.depends('lineas_venta.subtotal')
    def _compute_total(self):
        """
        Suma los subtotales de todas las líneas de la venta.
        Se recalcula automáticamente cuando cambia cualquier línea.
        """
        for rec in self:
            rec.total = sum(rec.lineas_venta.mapped('subtotal'))

    # ─── Constraint: venta debe tener al menos una línea ─────────────────────

    @api.constrains('lineas_venta')
    def _check_lineas(self):
        for rec in self:
            if rec.state == 'confirmada' and not rec.lineas_venta:
                raise ValidationError(
                    "No se puede confirmar una venta sin líneas de producto."
                )

    # ─── Acciones de botones ─────────────────────────────────────────────────

    def action_confirmar(self):
        for rec in self:
            if not rec.lineas_venta:
                raise ValidationError("Agregue al menos un producto antes de confirmar.")
            rec.state = 'confirmada'

    def action_cancelar(self):
        for rec in self:
            rec.state = 'cancelada'

    def action_borrador(self):
        for rec in self:
            rec.state = 'borrador'
