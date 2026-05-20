from odoo import models, fields, api
from datetime import datetime

class UniversidadCarrera(models.Model):
    _name = 'universidad.carrera'
    _description = 'Carrera Universitaria'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'codigo'
    codigo = fields.Char(string='Código de Carrera', required=True, help='Código único de la carrera')
    nombre = fields.Char(string='Nombre de la Carrera', required=True, help='Nombre completo de la carrera')
    descripcion = fields.Text(string='Descripción', help='Descripción detallada de la carrera')

    class UniqueCodigoConstraint(models.Constraint):
        _name = 'unique_codigo_carrera'
        _sql = [('codigo', 'unique', 'El código de carrera debe ser único')]
    duracion_semestres = fields.Integer(string='Duración (Semestres)', required=True, default=8, help='Número de semestres que dura la carrera')
    creditos_totales = fields.Integer(string='Créditos Totales', required=True, default=240, help='Total de créditos requeridos')
    estado = fields.Selection([('activa', 'Activa'), ('inactiva', 'Inactiva'), ('suspension', 'En Suspensión')], string='Estado', default='activa', tracking=True, help='Estado actual de la carrera')
    facultad = fields.Char(string='Facultad', help='Facultad o departamento')
    decano = fields.Char(string='Decano', help='Nombre del decano responsable')
    fecha_creacion = fields.Date(string='Fecha de Creación', default=fields.Date.today(), help='Fecha cuando se creó la carrera')
    logo = fields.Binary(string='Logo de la Carrera', help='Logo o imagen representativa')
    porcentaje_aceptacion = fields.Float(string='% Aceptación Estudiantes', help='Porcentaje de aceptación para nuevos estudiantes')
    sitio_web = fields.Char(string='Sitio Web', help='URL del sitio web de la carrera')
    requisitos = fields.Html(string='Requisitos', help='Requisitos formateados en HTML')
    estudiante_ids = fields.One2many(comodel_name='universidad.estudiante', inverse_name='carrera_id', string='Estudiantes', help='Estudiantes inscritos en esta carrera')
    materia_ids = fields.Many2many(comodel_name='universidad.materia', relation='carrera_materia_rel', column1='carrera_id', column2='materia_id', string='Materias', help='Materias que pertenecen a esta carrera')
    cantidad_estudiantes = fields.Integer(string='Cantidad de Estudiantes', compute='_compute_cantidad_estudiantes', store=True, help='Cantidad total de estudiantes')
    cantidad_materias = fields.Integer(string='Cantidad de Materias', compute='_compute_cantidad_materias', store=True, help='Cantidad total de materias')

    @api.depends('estudiante_ids')
    def _compute_cantidad_estudiantes(self):
        for record in self:
            record.cantidad_estudiantes = len(record.estudiante_ids)

    @api.depends('materia_ids')
    def _compute_cantidad_materias(self):
        for record in self:
            record.cantidad_materias = len(record.materia_ids)

    @api.constrains('duracion_semestres')
    def _validar_duracion(self):
        for record in self:
            if record.duracion_semestres <= 0 or record.duracion_semestres > 16:
                raise models.ValidationError('La duración debe estar entre 1 y 16 semestres')

    @api.constrains('creditos_totales')
    def _validar_creditos(self):
        for record in self:
            if record.creditos_totales < 60 or record.creditos_totales > 500:
                raise models.ValidationError('Los créditos deben estar entre 60 y 500')

    @api.constrains('porcentaje_aceptacion')
    def _validar_porcentaje(self):
        for record in self:
            if record.porcentaje_aceptacion and (record.porcentaje_aceptacion < 0 or record.porcentaje_aceptacion > 100):
                raise models.ValidationError('El porcentaje de aceptación debe estar entre 0 y 100')

    def obtener_informacion(self):
        return {'codigo': self.codigo, 'nombre': self.nombre, 'duracion': f'{self.duracion_semestres} semestres', 'creditos': self.creditos_totales, 'estudiantes': self.cantidad_estudiantes, 'materias': self.cantidad_materias, 'estado': self.estado}

    def agregar_materia(self, materia_id):
        self.write({'materia_ids': [(4, materia_id)]})

    def obtener_estudiantes_activos(self):
        return self.estudiante_ids.filtered(lambda e: e.activo)
