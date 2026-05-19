# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Produccion(models.Model):
    _name = 'plasticos.produccion'
    _description = 'Producción'
    _order = 'fecha_inicio desc'

    name = fields.Char(string='Orden', readonly=True, default='Nuevo')
    producto_id = fields.Many2one('plasticos.producto', string='Producto', required=True)
    cantidad = fields.Integer(string='Cantidad', default=1)
    producido = fields.Integer(string='Producido', default=0)
    fecha_inicio = fields.Date(string='Inicio', default=fields.Date.today)
    fecha_fin = fields.Date(string='Fin Estimada')
    estado = fields.Selection([
        ('borrador', 'Borrador'), ('programada', 'Programada'),
        ('en_proceso', 'En Proceso'), ('completada', 'Completada'), ('cancelada', 'Cancelada')
    ], string='Estado', default='borrador')
    prioridad = fields.Selection([
        ('baja', 'Baja'), ('media', 'Media'), ('alta', 'Alta'), ('urgente', 'Urgente')
    ], string='Prioridad', default='media')
    responsable = fields.Char(string='Responsable')
    observaciones = fields.Text(string='Observaciones')

    progreso = fields.Float(string='Progreso %', compute='_compute_progreso', store=True)

    @api.depends('cantidad', 'producido')
    def _compute_progreso(self):
        for p in self:
            p.progreso = (p.producido / p.cantidad * 100) if p.cantidad > 0 else 0

    @api.constrains('cantidad')
    def _check_cantidad(self):
        for p in self:
            if p.cantidad <= 0:
                raise ValidationError('La cantidad debe ser mayor a 0')

    @api.constrains('producido', 'cantidad')
    def _check_producido(self):
        for p in self:
            if p.producido > p.cantidad:
                raise ValidationError('Producido no puede ser mayor a la cantidad planeada')

    @api.onchange('cantidad')
    def _onchange_cantidad(self):
        if self.cantidad and self.cantidad > 500:
            return {'warning': {'title': 'Orden Grande', 'message': 'Verifique materia prima disponible'}}

    def action_programar(self):
        self.write({'estado': 'programada'})

    def action_iniciar(self):
        self.write({'estado': 'en_proceso'})

    def action_completar(self):
        for p in self:
            if p.producido < p.cantidad:
                raise ValidationError('Cantidad producida insuficiente')
            p.write({'estado': 'completada'})

    def action_cancelar(self):
        self.write({'estado': 'cancelada'})

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('plasticos.produccion') or 'PROD001'
        return super(Produccion, self).create(vals)
