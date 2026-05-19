from odoo import models, fields, api

class UniversidadMatricula(models.Model):
    _name = 'universidad.matricula'
    _description = 'Matrícula (Inscripción en Materia)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha_inscripcion desc'
    estudiante_id = fields.Many2one(comodel_name='universidad.estudiante', string='Estudiante', required=True, ondelete='cascade', help='Estudiante inscrito')
    materia_id = fields.Many2one(comodel_name='universidad.materia', string='Materia', required=True, ondelete='cascade', help='Materia en la cual se inscribe')
    numero_matricula = fields.Char(string='Número de Inscripción', required=True, help='Identificador único de la inscripción')

    class UniqueNumeroMatriculaMatriculaConstraint(models.Constraint):
        _name = 'unique_numero_matricula_matricula'
        _sql = [('numero_matricula', 'unique', 'El número de inscripción debe ser único')]
    fecha_inscripcion = fields.Date(string='Fecha de Inscripción', required=True, default=fields.Date.today(), help='Fecha cuando se realizó la inscripción')
    fecha_retiro = fields.Date(string='Fecha de Retiro', help='Fecha si se retira de la materia')
    calificacion = fields.Float(string='Calificación Final', default=0.0, help='Calificación final (0-100)', tracking=True)
    participacion = fields.Float(string='Participación (%)', default=0.0, help='Porcentaje de participación en clase')
    asistencia = fields.Float(string='Asistencia (%)', default=0.0, help='Porcentaje de asistencia')
    tareas = fields.Float(string='Calificación Tareas', default=0.0, help='Promedio de calificación en tareas')
    examenes = fields.Float(string='Calificación Exámenes', default=0.0, help='Promedio de exámenes')
    proyecto_final = fields.Float(string='Proyecto Final', default=0.0, help='Calificación del proyecto final')
    estado = fields.Selection([('inscrito', 'Inscrito'), ('cursando', 'Cursando'), ('calificado', 'Calificado'), ('retirado', 'Retirado'), ('reprobado', 'Reprobado'), ('aprobado', 'Aprobado')], string='Estado', default='inscrito', tracking=True, help='Estado de la matrícula')
    resultado = fields.Selection([('aprobado', 'Aprobado'), ('reprobado', 'Reprobado'), ('pendiente', 'Pendiente')], string='Resultado', compute='_compute_resultado', store=True, help='Resultado final de la materia')
    calificacion_ponderada = fields.Float(string='Calificación Ponderada', compute='_compute_calificacion_ponderada', store=True, help='Calificación ponderada con diferentes componentes')
    observaciones = fields.Text(string='Observaciones', help='Notas adicionales sobre el desempeño')
    creditos_ganados = fields.Integer(string='Créditos Ganados', compute='_compute_creditos_ganados', store=True, help='Créditos ganados si aprueba')
    nota_letra = fields.Char(string='Nota (Letra)', compute='_compute_nota_letra', store=False, help='Calificación en formato de letra (A, B, C, D, F)')

    @api.constrains('calificacion')
    def _validar_calificacion(self):
        for record in self:
            if record.calificacion < 0 or record.calificacion > 100:
                raise models.ValidationError('La calificación debe estar entre 0 y 100')

    @api.constrains('participacion', 'asistencia')
    def _validar_porcentajes(self):
        for record in self:
            if record.participacion and (record.participacion < 0 or record.participacion > 100):
                raise models.ValidationError('La participación debe estar entre 0 y 100%')
            if record.asistencia and (record.asistencia < 0 or record.asistencia > 100):
                raise models.ValidationError('La asistencia debe estar entre 0 y 100%')

    @api.constrains('asistencia')
    def _validar_asistencia_minima(self):
        for record in self:
            if record.asistencia and record.asistencia < 60:
                if record.resultado == 'aprobado':
                    raise models.ValidationError('La asistencia mínima debe ser 60% para aprobar')

    @api.constrains('fecha_retiro')
    def _validar_fecha_retiro(self):
        for record in self:
            if record.fecha_retiro and record.fecha_retiro < record.fecha_inscripcion:
                raise models.ValidationError('La fecha de retiro debe ser posterior a la inscripción')

    @api.onchange('calificacion')
    def _onchange_calificacion(self):
        if self.calificacion >= 70:
            self.estado = 'aprobado'
        elif self.calificacion > 0 and self.calificacion < 70:
            self.estado = 'reprobado'

    @api.onchange('tareas', 'examenes', 'proyecto_final')
    def _onchange_componentes(self):
        if self.tareas or self.examenes or self.proyecto_final:
            pass

    @api.depends('calificacion')
    def _compute_resultado(self):
        for record in self:
            if record.estado == 'retirado':
                record.resultado = 'pendiente'
            elif record.calificacion >= 70:
                record.resultado = 'aprobado'
            elif record.calificacion > 0:
                record.resultado = 'reprobado'
            else:
                record.resultado = 'pendiente'

    @api.depends('tareas', 'examenes', 'proyecto_final', 'participacion', 'asistencia')
    def _compute_calificacion_ponderada(self):
        for record in self:
            if record.tareas or record.examenes or record.proyecto_final:
                ponderada = record.tareas * 0.2 + record.examenes * 0.4 + record.proyecto_final * 0.3 + record.participacion * 0.1
                record.calificacion_ponderada = round(ponderada, 2)
            else:
                record.calificacion_ponderada = 0.0

    @api.depends('materia_id', 'resultado')
    def _compute_creditos_ganados(self):
        for record in self:
            if record.resultado == 'aprobado' and record.materia_id:
                record.creditos_ganados = record.materia_id.creditos
            else:
                record.creditos_ganados = 0

    @api.depends('calificacion')
    def _compute_nota_letra(self):
        for record in self:
            calificacion = record.calificacion
            if calificacion >= 90:
                record.nota_letra = 'A'
            elif calificacion >= 80:
                record.nota_letra = 'B'
            elif calificacion >= 70:
                record.nota_letra = 'C'
            elif calificacion >= 60:
                record.nota_letra = 'D'
            else:
                record.nota_letra = 'F'

    def obtener_resumen(self):
        return {'estudiante': self.estudiante_id.name, 'materia': self.materia_id.nombre, 'calificacion': self.calificacion, 'nota': self.nota_letra, 'resultado': self.resultado, 'creditos': self.creditos_ganados, 'estado': self.estado}

    def marcar_como_cursando(self):
        self.write({'estado': 'cursando'})

    def marcar_como_calificado(self):
        self.write({'estado': 'calificado'})

    def retirar_estudiante(self):
        today = fields.Date.today()
        self.write({'fecha_retiro': today, 'estado': 'retirado'})

    def calcular_calificacion_final(self):
        if not self.tareas and (not self.examenes) and (not self.proyecto_final):
            return 0.0
        total = 0
        contador = 0
        if self.tareas > 0:
            total += self.tareas
            contador += 1
        if self.examenes > 0:
            total += self.examenes
            contador += 1
        if self.proyecto_final > 0:
            total += self.proyecto_final
            contador += 1
        if contador > 0:
            return round(total / contador, 2)
        return 0.0
