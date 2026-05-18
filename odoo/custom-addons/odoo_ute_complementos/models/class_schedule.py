from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ClassSchedule(models.Model):
    _name = "ou.class.schedule"
    _description = "Horario de clase UTE"
    _order = "day_of_week, start_hour"

    name = fields.Char(string="Referencia", compute="_compute_name", store=True)
    teacher_id = fields.Many2one("ou.teacher", string="Docente", required=True)
    signature_id = fields.Many2one("ou.signature", string="Materia", required=True)
    classroom_id = fields.Many2one("ou.classroom", string="Aula", required=True)
    academic_plan_id = fields.Many2one("ou.academic.plan", string="Plan academico")
    day_of_week = fields.Selection(
        [
            ("1", "Lunes"),
            ("2", "Martes"),
            ("3", "Miercoles"),
            ("4", "Jueves"),
            ("5", "Viernes"),
            ("6", "Sabado"),
        ],
        string="Dia",
        required=True,
    )
    start_hour = fields.Float(string="Hora inicio", required=True)
    end_hour = fields.Float(string="Hora fin", required=True)
    duration = fields.Float(string="Duracion", compute="_compute_duration", store=True)
    modality = fields.Selection(
        [("presencial", "Presencial"), ("virtual", "Virtual"), ("hibrida", "Hibrida")],
        string="Modalidad",
        default="presencial",
    )
    active = fields.Boolean(string="Activo", default=True)
    observations = fields.Text(string="Observaciones")

    @api.depends("teacher_id", "signature_id", "day_of_week", "start_hour")
    def _compute_name(self):
        day_names = dict(self._fields["day_of_week"].selection)
        for schedule in self:
            day = day_names.get(schedule.day_of_week, "")
            teacher = schedule.teacher_id.full_name or schedule.teacher_id.name or ""
            signature = schedule.signature_id.name or ""
            schedule.name = "%s - %s - %s %.2f" % (teacher, signature, day, schedule.start_hour or 0.0)

    @api.depends("start_hour", "end_hour")
    def _compute_duration(self):
        for schedule in self:
            schedule.duration = schedule.end_hour - schedule.start_hour

    @api.onchange("academic_plan_id")
    def _onchange_academic_plan_id(self):
        if self.academic_plan_id:
            self.teacher_id = self.academic_plan_id.teacher_id
            self.signature_id = self.academic_plan_id.signature_id

    @api.constrains("start_hour", "end_hour")
    def _check_hours(self):
        for schedule in self:
            if schedule.start_hour < 0 or schedule.end_hour > 24:
                raise ValidationError("Las horas deben estar dentro del rango de 0 a 24.")
            if schedule.end_hour <= schedule.start_hour:
                raise ValidationError("La hora fin debe ser mayor que la hora inicio.")
