from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Attendance(models.Model):
    _name = "ou.attendance"
    _description = "Asistencia docente UTE"
    _order = "attendance_date desc"

    name = fields.Char(string="Referencia", compute="_compute_name", store=True)
    teacher_id = fields.Many2one("ou.teacher", string="Docente", required=True)
    schedule_id = fields.Many2one("ou.class.schedule", string="Horario")
    signature_id = fields.Many2one("ou.signature", string="Materia")
    attendance_date = fields.Date(string="Fecha", default=fields.Date.context_today, required=True)
    check_in = fields.Float(string="Hora entrada")
    check_out = fields.Float(string="Hora salida")
    worked_hours = fields.Float(string="Horas trabajadas", compute="_compute_worked_hours", store=True)
    status = fields.Selection(
        [
            ("present", "Presente"),
            ("late", "Atrasado"),
            ("absent", "Ausente"),
            ("justified", "Justificado"),
        ],
        string="Estado",
        default="present",
        required=True,
    )
    justified = fields.Boolean(string="Justificado")
    notes = fields.Text(string="Notas")

    @api.depends("teacher_id", "attendance_date")
    def _compute_name(self):
        for attendance in self:
            teacher = attendance.teacher_id.full_name or attendance.teacher_id.name or ""
            attendance.name = "%s - %s" % (teacher, attendance.attendance_date or "")

    @api.depends("check_in", "check_out")
    def _compute_worked_hours(self):
        for attendance in self:
            attendance.worked_hours = max(attendance.check_out - attendance.check_in, 0.0)

    @api.onchange("schedule_id")
    def _onchange_schedule_id(self):
        if self.schedule_id:
            self.teacher_id = self.schedule_id.teacher_id
            self.signature_id = self.schedule_id.signature_id
            self.check_in = self.schedule_id.start_hour
            self.check_out = self.schedule_id.end_hour

    @api.constrains("check_in", "check_out")
    def _check_attendance_hours(self):
        for attendance in self:
            if attendance.check_in < 0 or attendance.check_out > 24:
                raise ValidationError("Las horas deben estar dentro del rango de 0 a 24.")
            if attendance.check_out and attendance.check_out < attendance.check_in:
                raise ValidationError("La hora de salida no puede ser menor que la hora de entrada.")
