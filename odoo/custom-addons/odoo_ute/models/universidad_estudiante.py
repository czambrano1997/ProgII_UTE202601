from odoo import models, fields, api
from odoo.exceptions import ValidationError

class UniversidadEstudiante(models.Model):
    _name = 'universidad.estudiante'
    _description = 'Estudiante Universitario'
    _inherit = ['universidad.persona', 'mail.thread', 'mail.activity.mixin']
    _order = 'numero_matricula'
    numero_matricula = fields.Char(string='Número de Matrícula', required=True, help='Identificador único del estudiante')

    @api.constrains('numero_matricula')
    def _check_unique_numero_matricula(self):
        for record in self:
            if record.numero_matricula:
                duplicate = self.search([('numero_matricula', '=', record.numero_matricula), ('id', '!=', record.id)], limit=1)
                if duplicate:
                    raise ValidationError('El número de matrícula debe ser único')
    carrera_id = fields.Many2one(comodel_name='universidad.carrera', string='Carrera', required=True, help='Carrera en la que está inscrito')
    semestre_actual = fields.Integer(string='Semestre Actual', required=True, default=1, help='Semestre en el que se encuentra')
    promedio_academico = fields.Float(string='Promedio Académico', compute='_compute_promedio_academico', store=True, help='Promedio de todas las calificaciones')
    total_creditos_aprobados = fields.Integer(string='Créditos Aprobados', compute='_compute_creditos_aprobados', store=True, help='Total de créditos aprobados')
    estado_estudiante = fields.Selection([('activo', 'Activo'), ('inactivo', 'Inactivo'), ('graduado', 'Graduado'), ('expulsado', 'Expulsado'), ('suspension_temporal', 'Suspensión Temporal')], string='Estado del Estudiante', default='activo', tracking=True, help='Estado académico actual')
    fecha_ingreso = fields.Date(string='Fecha de Ingreso', required=True, default=fields.Date.context_today, help='Fecha cuando ingresó a la universidad')
    matricula_ids = fields.One2many(comodel_name='universidad.matricula', inverse_name='estudiante_id', string='Matrículas', help='Historial de matrículas en materias')
    materia_ids = fields.Many2many(comodel_name='universidad.materia', relation='estudiante_materia_rel', column1='estudiante_id', column2='materia_id', string='Materias Inscritas', help='Materias en las que está inscrito')
    monto_deuda = fields.Monetary(string='Monto de Deuda', currency_field='currency_id', default=0.0, help='Deuda pendiente del estudiante')
    currency_id = fields.Many2one(comodel_name='res.currency', string='Moneda', default=lambda self: self.env.company.currency_id.id, help='Moneda para transacciones')
    especialidad = fields.Char(string='Especialidad o Concentración', help='Especialización dentro de la carrera')
    numero_expediente = fields.Char(string='Número de Expediente', help='Número del expediente administrativo')

    @api.depends('matricula_ids.calificacion')
    def _compute_promedio_academico(self):
        for record in self:
            matriculas = record.matricula_ids.filtered(lambda m: m.calificacion and m.calificacion > 0)
            if matriculas:
                promedio = sum((m.calificacion for m in matriculas)) / len(matriculas)
                record.promedio_academico = round(promedio, 2)
            else:
                record.promedio_academico = 0.0

    @api.depends('matricula_ids.materia_id.creditos')
    def _compute_creditos_aprobados(self):
        for record in self:
            creditos = sum((m.materia_id.creditos for m in record.matricula_ids if m.calificacion and m.calificacion >= 70))
            record.total_creditos_aprobados = creditos

    @api.constrains('semestre_actual')
    def _validar_semestre(self):
        for record in self:
            if record.carrera_id:
                max_semestres = record.carrera_id.duracion_semestres
                if record.semestre_actual < 1 or record.semestre_actual > max_semestres:
                    raise ValidationError(f'El semestre debe estar entre 1 y {max_semestres}')

    @api.constrains('promedio_academico')
    def _validar_promedio_para_graduacion(self):
        for record in self:
            if record.estado_estudiante == 'graduado' and record.promedio_academico < 70:
                raise ValidationError('Un estudiante graduado debe tener promedio mínimo de 70')

    @api.onchange('carrera_id')
    def _onchange_carrera(self):
        if self.carrera_id:
            self.semestre_actual = 1

    @api.onchange('promedio_academico')
    def _onchange_promedio_para_estado(self):
        if self.promedio_academico and self.promedio_academico < 60:
            return {'warning': {'title': 'Promedio Bajo', 'message': 'El estudiante tiene un promedio bajo. Considere revisar su estado.'}}

    def obtener_descripcion(self):
        carrera = self.carrera_id.nombre if self.carrera_id else 'Sin carrera'
        return f'Estudiante de {carrera} (Semestre {self.semestre_actual}) - Matricula: {self.numero_matricula}'

    def puede_graduarse(self):
        self.ensure_one()
        if self.estado_estudiante == 'expulsado':
            return False
        if not self.carrera_id:
            return False
        if self.semestre_actual < self.carrera_id.duracion_semestres:
            return False
        if self.promedio_academico < 70:
            return False
        if self.total_creditos_aprobados < self.carrera_id.creditos_totales:
            return False
        return True

    def obtener_resumen_academico(self):
        return {'nombre': self.name, 'carrera': self.carrera_id.nombre if self.carrera_id else 'N/A', 'semestre': self.semestre_actual, 'promedio': self.promedio_academico, 'creditos_aprobados': self.total_creditos_aprobados, 'estado': self.estado_estudiante, 'puede_graduarse': self.puede_graduarse(), 'deuda': self.monto_deuda}

    def inscribir_en_materia(self, materia_id):
        for student in self:
            student.write({'materia_ids': [(4, materia_id)]})
            self.env['universidad.matricula'].create({'estudiante_id': student.id, 'materia_id': materia_id, 'calificacion': 0})
