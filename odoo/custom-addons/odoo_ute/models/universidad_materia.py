from odoo import models, fields, api
from odoo.exceptions import ValidationError

class UniversidadMateria(models.Model):
    _name = 'universidad.materia'
    _description = 'Materia Universitaria'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'codigo'
    codigo = fields.Char(string='Código de Materia', required=True, help='Código único de la materia')

    @api.constrains('codigo')
    def _check_unique_codigo_materia(self):
        for record in self:
            if record.codigo:
                duplicate = self.search([('codigo', '=', record.codigo), ('id', '!=', record.id)], limit=1)
                if duplicate:
                    raise ValidationError('El código de la materia debe ser único')
    nombre = fields.Char(string='Nombre de la Materia', required=True, help='Nombre completo de la materia')
    descripcion = fields.Text(string='Descripción', help='Descripción del contenido de la materia')
    creditos = fields.Integer(string='Créditos', required=True, default=3, help='Cantidad de créditos académicos')
    horas_semanales = fields.Integer(string='Horas Semanales', required=True, default=4, help='Horas de clase por semana')
    semestre = fields.Integer(string='Semestre', required=True, help='En qué semestre se ofrece')
    prerequisitos = fields.Text(string='Prerequisitos', help='Materias que deben ser aprobadas antes')
    profesor_id = fields.Many2one(comodel_name='universidad.profesor', string='Profesor', required=True, help='Profesor que imparte la materia')
    carrera_ids = fields.Many2many(comodel_name='universidad.carrera', relation='carrera_materia_rel', column1='materia_id', column2='carrera_id', string='Carreras', help='Carreras a las que pertenece')
    estudiante_ids = fields.Many2many(comodel_name='universidad.estudiante', relation='estudiante_materia_rel', column1='materia_id', column2='estudiante_id', string='Estudiantes Inscritos', help='Estudiantes inscritos en esta materia')
    matricula_ids = fields.One2many(comodel_name='universidad.matricula', inverse_name='materia_id', string='Matrículas', help='Registros de matrículas en esta materia')
    estado = fields.Selection([('activa', 'Activa'), ('inactiva', 'Inactiva'), ('retirada', 'Retirada'), ('suspension', 'En Suspensión')], string='Estado', default='activa', tracking=True, help='Estado actual de la materia')
    semestre_oferta = fields.Char(string='Semestre de Oferta', help='Ej: 2024-A, 2024-B')
    cantidad_estudiantes = fields.Integer(string='Cantidad de Estudiantes', compute='_compute_cantidad_estudiantes', store=True, help='Número total de estudiantes inscritos')
    promedio_calificaciones = fields.Float(string='Promedio de Calificaciones', compute='_compute_promedio_calificaciones', store=True, help='Promedio de todas las calificaciones en esta materia')
    estudiantes_aprobados = fields.Integer(string='Estudiantes Aprobados', compute='_compute_estudiantes_aprobados', store=True, help='Cantidad de estudiantes con nota >= 70')
    porcentaje_aprobacion = fields.Float(string='% Aprobación', compute='_compute_porcentaje_aprobacion', store=True, help='Porcentaje de estudiantes aprobados')

    @api.depends('estudiante_ids')
    def _compute_cantidad_estudiantes(self):
        for record in self:
            record.cantidad_estudiantes = len(record.estudiante_ids)

    @api.depends('matricula_ids.calificacion')
    def _compute_promedio_calificaciones(self):
        for record in self:
            matriculas = record.matricula_ids.filtered(lambda m: m.calificacion and m.calificacion > 0)
            if matriculas:
                promedio = sum((m.calificacion for m in matriculas)) / len(matriculas)
                record.promedio_calificaciones = round(promedio, 2)
            else:
                record.promedio_calificaciones = 0.0

    @api.depends('matricula_ids.calificacion')
    def _compute_estudiantes_aprobados(self):
        for record in self:
            aprobados = len(record.matricula_ids.filtered(lambda m: m.calificacion and m.calificacion >= 70))
            record.estudiantes_aprobados = aprobados

    @api.depends('cantidad_estudiantes', 'estudiantes_aprobados')
    def _compute_porcentaje_aprobacion(self):
        for record in self:
            if record.cantidad_estudiantes > 0:
                record.porcentaje_aprobacion = record.estudiantes_aprobados / record.cantidad_estudiantes * 100
            else:
                record.porcentaje_aprobacion = 0.0

    @api.constrains('creditos')
    def _validar_creditos(self):
        for record in self:
            if record.creditos <= 0 or record.creditos > 10:
                raise ValidationError('Los créditos deben estar entre 1 y 10')

    @api.constrains('horas_semanales')
    def _validar_horas_semanales(self):
        for record in self:
            if record.horas_semanales < 2 or record.horas_semanales > 10:
                raise ValidationError('Las horas semanales deben estar entre 2 y 10')

    @api.constrains('semestre')
    def _validar_semestre(self):
        for record in self:
            if record.semestre < 1 or record.semestre > 16:
                raise ValidationError('El semestre debe estar entre 1 y 16')

    @api.constrains('profesor_id')
    def _validar_profesor_activo(self):
        for record in self:
            if record.profesor_id and record.profesor_id.estado_profesor != 'activo':
                raise ValidationError('El profesor debe estar activo para imparta materias')

    @api.onchange('creditos')
    def _onchange_creditos_horas(self):
        if self.creditos:
            self.horas_semanales = self.creditos

    def obtener_informacion(self):
        return {'codigo': self.codigo, 'nombre': self.nombre, 'profesor': self.profesor_id.name if self.profesor_id else 'N/A', 'creditos': self.creditos, 'semestre': self.semestre, 'estudiantes': self.cantidad_estudiantes, 'promedio': self.promedio_calificaciones, 'aprobacion': f'{self.porcentaje_aprobacion:.1f}%'}

    def inscribir_estudiante(self, estudiante_id):
        self.write({'estudiante_ids': [(4, estudiante_id)]})
        self.env['universidad.matricula'].create({'estudiante_id': estudiante_id, 'materia_id': self.id, 'calificacion': 0})

    def calcular_estadisticas(self):
        matriculas = self.matricula_ids.filtered(lambda m: m.calificacion and m.calificacion > 0)
        if not matriculas:
            return {'total_estudiantes': self.cantidad_estudiantes, 'aprobados': 0, 'reprobados': 0, 'promedio': 0, 'nota_maxima': 0, 'nota_minima': 0}
        calificaciones = [m.calificacion for m in matriculas]
        return {'total_estudiantes': self.cantidad_estudiantes, 'aprobados': self.estudiantes_aprobados, 'reprobados': len(matriculas) - self.estudiantes_aprobados, 'promedio': round(sum(calificaciones) / len(calificaciones), 2), 'nota_maxima': max(calificaciones), 'nota_minima': min(calificaciones)}
