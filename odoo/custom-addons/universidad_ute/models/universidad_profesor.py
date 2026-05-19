from odoo import models, fields, api

class UniversidadProfesor(models.Model):
    _name = 'universidad.profesor'
    _description = 'Profesor Universitario'
    _inherit = ['universidad.persona', 'mail.thread', 'mail.activity.mixin']
    _order = 'codigo_profesor'
    codigo_profesor = fields.Char(string='Código de Profesor', required=True, help='Identificador único del profesor')
    titulo_academico = fields.Selection([('licenciatura', 'Licenciatura'), ('maestria', 'Maestría'), ('doctorado', 'Doctorado'), ('postdoctorado', 'Postdoctorado')], string='Título Académico Máximo', required=True, help='Máximo título académico obtenido')
    especialidad = fields.Char(string='Especialidad', required=True, help='Área de especialización del profesor')
    tipo_contrato = fields.Selection([('tiempo_completo', 'Tiempo Completo'), ('medio_tiempo', 'Medio Tiempo'), ('por_horas', 'Por Horas'), ('temporal', 'Temporal')], string='Tipo de Contrato', required=True, default='tiempo_completo', help='Modalidad de contratación')
    fecha_contratacion = fields.Date(string='Fecha de Contratación', required=True, default=fields.Date.today(), help='Fecha cuando fue contratado')
    numero_empleado = fields.Char(string='Número de Empleado', help='Identificador de empleado')

    class UniqueCodigoProfesorConstraint(models.Constraint):
        _name = 'unique_codigo_profesor'
        _sql = [('codigo_profesor', 'unique', 'El código de profesor debe ser único')]

    class UniqueNumeroEmpleadoConstraint(models.Constraint):
        _name = 'unique_numero_empleado'
        _sql = [('numero_empleado', 'unique', 'El número de empleado debe ser único')]
    departamento = fields.Char(string='Departamento', help='Departamento donde trabaja')
    despacho = fields.Char(string='Despacho/Oficina', help='Ubicación de la oficina')
    extension_telefonica = fields.Char(string='Extensión Telefónica', help='Extensión dentro de la universidad')
    salario_base = fields.Monetary(string='Salario Base', currency_field='currency_id', help='Salario mensual base')
    currency_id = fields.Many2one(comodel_name='res.currency', string='Moneda', default=lambda self: self.env.company.currency_id, help='Moneda para salario')
    calificacion_docente = fields.Float(string='Calificación Docente', compute='_compute_calificacion_docente', store=True, help='Promedio de calificaciones de estudiantes')
    horas_semanales = fields.Integer(string='Horas Semanales de Clase', default=20, help='Cantidad de horas de clase por semana')
    anos_experiencia = fields.Integer(string='Años de Experiencia', compute='_compute_anos_experiencia', store=False, help='Años desde la contratación')
    estado_profesor = fields.Selection([('activo', 'Activo'), ('inactivo', 'Inactivo'), ('licencia', 'Licencia'), ('retirado', 'Retirado')], string='Estado del Profesor', default='activo', tracking=True, help='Estado laboral actual')
    materia_ids = fields.One2many(comodel_name='universidad.materia', inverse_name='profesor_id', string='Materias Impartidas', help='Materias que enseña')
    cv = fields.Binary(string='Curriculum Vitae', help='Documento de CV')
    nombre_cv = fields.Char(string='Nombre del CV', help='Nombre del archivo')
    certificaciones = fields.Html(string='Certificaciones', help='Lista de certificaciones profesionales')
    universidad_educacion = fields.Char(string='Universidad de Educación', help='Donde cursó sus estudios')

    @api.depends('materia_ids.promedio_calificaciones')
    def _compute_calificacion_docente(self):
        for record in self:
            if record.materia_ids:
                calificaciones = [m.promedio_calificaciones for m in record.materia_ids if m.promedio_calificaciones]
                if calificaciones:
                    record.calificacion_docente = sum(calificaciones) / len(calificaciones)
                else:
                    record.calificacion_docente = 0.0
            else:
                record.calificacion_docente = 0.0

    @api.depends('fecha_contratacion')
    def _compute_anos_experiencia(self):
        from datetime import datetime
        for record in self:
            if record.fecha_contratacion:
                today = fields.Date.today()
                anos = today.year - record.fecha_contratacion.year
                if (today.month, today.day) < (record.fecha_contratacion.month, record.fecha_contratacion.day):
                    anos -= 1
                record.anos_experiencia = anos
            else:
                record.anos_experiencia = 0

    @api.constrains('horas_semanales')
    def _validar_horas_semanales(self):
        for record in self:
            if record.tipo_contrato == 'tiempo_completo' and record.horas_semanales < 20:
                raise models.ValidationError('Un profesor de tiempo completo debe tener mínimo 20 horas semanales')
            if record.tipo_contrato == 'medio_tiempo' and record.horas_semanales > 20:
                raise models.ValidationError('Un profesor de medio tiempo no puede exceder 20 horas semanales')

    @api.constrains('salario_base')
    def _validar_salario(self):
        for record in self:
            if record.salario_base and record.salario_base < 0:
                raise models.ValidationError('El salario no puede ser negativo')

    @api.constrains('titulo_academico')
    def _validar_titulo_salario(self):
        for record in self:
            if record.titulo_academico == 'doctorado' and record.salario_base:
                if record.salario_base < 2000:
                    raise models.ValidationError('Profesores con doctorado deben tener salario mínimo de $2000')

    @api.onchange('titulo_academico')
    def _onchange_titulo_academico(self):
        if self.titulo_academico == 'doctorado':
            return {'warning': {'title': 'Profesor con Doctorado', 'message': 'Profesor calificado para investigación y proyectos avanzados.'}}

    @api.onchange('tipo_contrato')
    def _onchange_contrato(self):
        if self.tipo_contrato == 'tiempo_completo':
            self.horas_semanales = 40
        elif self.tipo_contrato == 'medio_tiempo':
            self.horas_semanales = 20
        elif self.tipo_contrato == 'por_horas':
            self.horas_semanales = 10

    def obtener_descripcion(self):
        return f'Profesor de {self.especialidad} ({self.titulo_academico.upper()}) - {self.codigo_profesor}'

    def obtener_informacion_laboral(self):
        return {'nombre': self.name, 'codigo': self.codigo_profesor, 'especialidad': self.especialidad, 'titulo': self.titulo_academico, 'contrato': self.tipo_contrato, 'horas_semanales': self.horas_semanales, 'anos_experiencia': self.anos_experiencia, 'salario': self.salario_base, 'calificacion': self.calificacion_docente, 'estado': self.estado_profesor}

    def puede_impartir_materia(self):
        if self.estado_profesor != 'activo':
            return False
        if not self.especialidad:
            return False
        return True

    def agregar_materia(self, materia_id):
        self.write({'materia_ids': [(4, materia_id)]})

    def obtener_materias_impartidas(self):
        return self.materia_ids.mapped('nombre')
