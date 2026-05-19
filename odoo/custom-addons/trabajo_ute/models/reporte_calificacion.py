# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ReporteCalificacion(models.Model):
    _name = 'ou.reporte.calificacion'
    _description = 'Reporte Consolidado de Calificaciones'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha_generacion desc'

    name = fields.Char(string='Nombre del Reporte', required=True, tracking=True)
    code = fields.Char(string='Código', required=True, copy=False)
    fecha_generacion = fields.Datetime(string='Fecha de Generación', default=fields.Datetime.now, readonly=True)
    periodo_id = fields.Many2one(
        'ou.periodo.evaluacion',
        string='Período de Evaluación',
        required=True,
        tracking=True
    )
    tipo_reporte = fields.Selection([
        ('conductores', 'Conductores'),
        ('vehiculos', 'Vehículos'),
        ('consolidado', 'Consolidado'),
    ], string='Tipo de Reporte', required=True, default='consolidado')
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('generado', 'Generado'),
        ('publicado', 'Publicado'),
        ('archivado', 'Archivado'),
    ], string='Estado', default='borrador', tracking=True)
    
    # Campos de resumen computados
    total_evaluados = fields.Integer(
        string='Total Evaluados',
        compute='_compute_resumen',
        store=True
    )
    promedio_general = fields.Float(
        string='Promedio General',
        compute='_compute_resumen',
        store=True
    )
    mejores_calificados = fields.Integer(
        string='Mejores Calificados (A)',
        compute='_compute_resumen',
        store=True
    )
    peores_calificados = fields.Integer(
        string='Calificados Deficientes (F)',
        compute='_compute_resumen',
        store=True
    )
    
    # Campos relacionales
    linea_reporte_ids = fields.One2many(
        'ou.reporte.calificacion.linea',
        'reporte_id',
        string='Detalle del Reporte'
    )
    archivo_pdf = fields.Binary(string='Archivo PDF', attachment=True)
    nombre_archivo = fields.Char(string='Nombre Archivo')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', False):
                continue
            vals['code'] = self.env['ir.sequence'].next_by_code('ou.reporte.calificacion') or 'REP-000'
        return super(ReporteCalificacion, self).create(vals_list)

    @api.depends('periodo_id', 'tipo_reporte', 'linea_reporte_ids')
    def _compute_resumen(self):
        for record in self:
            if not record.periodo_id:
                record.total_evaluados = 0
                record.promedio_general = 0.0
                record.mejores_calificados = 0
                record.peores_calificados = 0
                continue
            
            lineas = record.linea_reporte_ids
            record.total_evaluados = len(lineas)
            
            if lineas:
                record.promedio_general = sum(lineas.mapped('promedio')) / len(lineas)
                record.mejores_calificados = len(lineas.filtered(lambda l: l.promedio >= 9))
                record.peores_calificados = len(lineas.filtered(lambda l: l.promedio < 6))
            else:
                record.promedio_general = 0.0
                record.mejores_calificados = 0
                record.peores_calificados = 0

    @api.constrains('periodo_id', 'tipo_reporte')
    def _check_reporte_unico(self):
        for record in self:
            if self.search_count([
                ('periodo_id', '=', record.periodo_id.id),
                ('tipo_reporte', '=', record.tipo_reporte),
                ('id', '!=', record.id),
                ('state', '!=', 'archivado')
            ]) > 0:
                raise ValidationError('Ya existe un reporte activo para este período y tipo.')

    @api.onchange('periodo_id')
    def _onchange_periodo_id(self):
        if self.periodo_id:
            self.name = f"Reporte {self.tipo_reporte.title()} - {self.periodo_id.name}"

    def action_generar(self):
        for record in self:
            # Lógica para generar líneas de reporte
            record._generar_lineas()
            record.state = 'generado'
            record.fecha_generacion = fields.Datetime.now()

    def _generar_lineas(self):
        self.ensure_one()
        self.linea_reporte_ids.unlink()
        
        if self.tipo_reporte in ['conductores', 'consolidado']:
            calificaciones = self.env['ou.calificacion.conductor'].search([
                ('periodo_id', '=', self.periodo_id.id),
                ('state', '=', 'aprobado')
            ])
            for cal in calificaciones:
                self.env['ou.reporte.calificacion.linea'].create({
                    'reporte_id': self.id,
                    'tipo_entidad': 'conductor',
                    'entidad_id': cal.conductor_id.id,
                    'nombre_entidad': cal.conductor_id.name,
                    'puntaje_total': cal.puntaje_total,
                    'promedio': cal.promedio,
                    'calificacion': cal.calificacion_letra,
                    'observacion': cal.observaciones,
                })
        
        if self.tipo_reporte in ['vehiculos', 'consolidado']:
            calificaciones = self.env['ou.calificacion.vehiculo'].search([
                ('periodo_id', '=', self.periodo_id.id),
                ('state', '=', 'aprobado')
            ])
            for cal in calificaciones:
                self.env['ou.reporte.calificacion.linea'].create({
                    'reporte_id': self.id,
                    'tipo_entidad': 'vehiculo',
                    'entidad_id': cal.vehiculo_id.id,
                    'nombre_entidad': cal.vehiculo_id.name,
                    'puntaje_total': cal.puntaje_total,
                    'promedio': cal.promedio,
                    'calificacion': dict(self.env['ou.calificacion.vehiculo']._fields['estado_general'].selection).get(cal.estado_general),
                    'observacion': cal.observaciones,
                })

    def action_publicar(self):
        for record in self:
            record.state = 'publicado'

    def action_archivar(self):
        for record in self:
            record.state = 'archivado'

    def action_regenerar(self):
        for record in self:
            record._generar_lineas()
            record.fecha_generacion = fields.Datetime.now()


class ReporteCalificacionLinea(models.Model):
    _name = 'ou.reporte.calificacion.linea'
    _description = 'Línea de Reporte de Calificación'
    _order = 'promedio desc'

    reporte_id = fields.Many2one(
        'ou.reporte.calificacion',
        string='Reporte',
        required=True,
        ondelete='cascade'
    )
    tipo_entidad = fields.Selection([
        ('conductor', 'Conductor'),
        ('vehiculo', 'Vehículo'),
    ], string='Tipo de Entidad', required=True)
    entidad_id = fields.Integer(string='ID Entidad', required=True)
    nombre_entidad = fields.Char(string='Nombre', required=True)
    puntaje_total = fields.Float(string='Puntaje Total', default=0.0)
    promedio = fields.Float(string='Promedio', default=0.0)
    calificacion = fields.Char(string='Calificación')
    observacion = fields.Text(string='Observación')
<<<<<<< HEAD
    ranking = fields.Integer(string='Ranking', default=0)
=======
    ranking = fields.Integer(string='Ranking', default=0)
    
>>>>>>> c1b48e8873a20a5a1324a750d1a52238c1f0fcc6
