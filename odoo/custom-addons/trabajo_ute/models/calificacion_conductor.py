# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CalificacionConductor(models.Model):
    _name = 'ou.calificacion.conductor'
    _description = 'Calificación de Conductor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha_evaluacion desc'

    name = fields.Char(string='Referencia', required=True, copy=False, default='Nuevo')
    periodo_id = fields.Many2one(
        'ou.periodo.evaluacion',
        string='Período de Evaluación',
        required=True,
        tracking=True
    )
    conductor_id = fields.Many2one(
        'ou.conductores',
        string='Conductor',
        required=True,
        tracking=True
    )
    fecha_evaluacion = fields.Date(string='Fecha de Evaluación', required=True, default=fields.Date.today)
    evaluador_id = fields.Many2one(
        'res.users',
        string='Evaluador',
        default=lambda self: self.env.user,
        required=True
    )
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('calificado', 'Calificado'),
        ('revisado', 'Revisado'),
        ('aprobado', 'Aprobado'),
    ], string='Estado', default='borrador', tracking=True)
    observaciones = fields.Text(string='Observaciones')
    
    # Campos de calificación numérica
    puntaje_puntualidad = fields.Float(string='Puntualidad (0-10)', default=0.0)
    puntaje_conducta = fields.Float(string='Conducta (0-10)', default=0.0)
    puntaje_cumplimiento = fields.Float(string='Cumplimiento Normas (0-10)', default=0.0)
    puntaje_mantenimiento = fields.Float(string='Cuidado Vehículo (0-10)', default=0.0)
    puntaje_productividad = fields.Float(string='Productividad (0-10)', default=0.0)
    
    # Campos computados
    puntaje_total = fields.Float(
        string='Puntaje Total',
        compute='_compute_puntaje_total',
        store=True
    )
    promedio = fields.Float(
        string='Promedio',
        compute='_compute_promedio',
        store=True
    )
    calificacion_letra = fields.Char(
        string='Calificación',
        compute='_compute_calificacion_letra',
        store=True
    )
    color_calificacion = fields.Integer(
        string='Color',
        compute='_compute_color_calificacion',
        store=True
    )
    
    # Campos relacionales
    linea_detalle_ids = fields.One2many(
        'ou.calificacion.conductor.linea',
        'calificacion_id',
        string='Detalle por Indicador'
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code('ou.calificacion.conductor') or 'Nuevo'
        return super(CalificacionConductor, self).create(vals_list)

    @api.depends('puntaje_puntualidad', 'puntaje_conducta', 'puntaje_cumplimiento', 
                 'puntaje_mantenimiento', 'puntaje_productividad')
    def _compute_puntaje_total(self):
        for record in self:
            record.puntaje_total = (
                record.puntaje_puntualidad +
                record.puntaje_conducta +
                record.puntaje_cumplimiento +
                record.puntaje_mantenimiento +
                record.puntaje_productividad
            )

    @api.depends('puntaje_total')
    def _compute_promedio(self):
        for record in self:
            record.promedio = record.puntaje_total / 5.0

    @api.depends('promedio')
    def _compute_calificacion_letra(self):
        for record in self:
            if record.promedio >= 9:
                record.calificacion_letra = 'A - Excelente'
            elif record.promedio >= 8:
                record.calificacion_letra = 'B - Muy Bueno'
            elif record.promedio >= 7:
                record.calificacion_letra = 'C - Bueno'
            elif record.promedio >= 6:
                record.calificacion_letra = 'D - Regular'
            else:
                record.calificacion_letra = 'F - Deficiente'

    @api.depends('promedio')
    def _compute_color_calificacion(self):
        for record in self:
            if record.promedio >= 9:
                record.color_calificacion = 10  # Verde
            elif record.promedio >= 7:
                record.color_calificacion = 3   # Amarillo
            elif record.promedio >= 6:
                record.color_calificacion = 2   # Naranja
            else:
                record.color_calificacion = 1   # Rojo

    @api.constrains('puntaje_puntualidad', 'puntaje_conducta', 'puntaje_cumplimiento',
                    'puntaje_mantenimiento', 'puntaje_productividad')
    def _check_puntajes_rango(self):
        for record in self:
            campos = [
                ('Puntualidad', record.puntaje_puntualidad),
                ('Conducta', record.puntaje_conducta),
                ('Cumplimiento', record.puntaje_cumplimiento),
                ('Mantenimiento', record.puntaje_mantenimiento),
                ('Productividad', record.puntaje_productividad),
            ]
            for nombre, valor in campos:
                if valor < 0 or valor > 10:
                    raise ValidationError(f'El puntaje de {nombre} debe estar entre 0 y 10.')

    @api.constrains('periodo_id', 'conductor_id')
    def _check_unica_calificacion_periodo(self):
        for record in self:
            if self.search_count([
                ('periodo_id', '=', record.periodo_id.id),
                ('conductor_id', '=', record.conductor_id.id),
                ('id', '!=', record.id)
            ]) > 0:
                raise ValidationError('Ya existe una calificación para este conductor en el período seleccionado.')

    @api.onchange('periodo_id')
    def _onchange_periodo_id(self):
        if self.periodo_id and self.periodo_id.state != 'en_proceso':
            return {'warning': {
                'title': 'Período no vigente',
                'message': 'El período seleccionado no está en estado "En Proceso". Las calificaciones deben realizarse en períodos vigentes.'
            }}

    def action_calificar(self):
        for record in self:
            record.state = 'calificado'

    def action_revisar(self):
        for record in self:
            record.state = 'revisado'

    def action_aprobar(self):
        for record in self:
            record.state = 'aprobado'


class CalificacionConductorLinea(models.Model):
    _name = 'ou.calificacion.conductor.linea'
    _description = 'Línea de Detalle de Calificación'

    calificacion_id = fields.Many2one(
        'ou.calificacion.conductor',
        string='Calificación',
        required=True,
        ondelete='cascade'
    )
    categoria_id = fields.Many2one(
        'ou.indicador.categoria',
        string='Categoría',
        required=True,
        domain=[('tipo_indicador', 'in', ['conductor', 'general'])]
    )
    puntaje_obtenido = fields.Float(string='Puntaje Obtenido', required=True, default=0.0)
    puntaje_maximo = fields.Float(
        string='Puntaje Máximo',
        related='categoria_id.peso_porcentaje',
        store=True
    )
    porcentaje_logrado = fields.Float(
        string='% Logrado',
        compute='_compute_porcentaje',
        store=True
    )
    observacion = fields.Text(string='Observación')

    @api.depends('puntaje_obtenido', 'puntaje_maximo')
    def _compute_porcentaje(self):
        for record in self:
            if record.puntaje_maximo > 0:
                record.porcentaje_logrado = (record.puntaje_obtenido / record.puntaje_maximo) * 100
            else:
                record.porcentaje_logrado = 0.0

    @api.constrains('puntaje_obtenido')
    def _check_puntaje_positivo(self):
        for record in self:
            if record.puntaje_obtenido < 0:
                raise ValidationError('El puntaje obtenido no puede ser negativo.')
            if record.puntaje_maximo > 0 and record.puntaje_obtenido > record.puntaje_maximo:
                raise ValidationError('El puntaje obtenido no puede superar el puntaje máximo de la categoría.')