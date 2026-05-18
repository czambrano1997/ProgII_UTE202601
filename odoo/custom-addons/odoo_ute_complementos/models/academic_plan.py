from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AcademicPlan(models.Model):
    _name = "ou.academic.plan"
    _description = "Planificacion academica docente"
    _order = "period desc, teacher_id"

    name = fields.Char(string="Nombre del plan", required=True)
    teacher_id = fields.Many2one("ou.teacher", string="Docente", required=True)
    signature_id = fields.Many2one("ou.signature", string="Materia", required=True)
    period = fields.Selection(
        [
            ("2026_1", "2026 - Primer periodo"),
            ("2026_2", "2026 - Segundo periodo"),
            ("2027_1", "2027 - Primer periodo"),
        ],
        string="Periodo",
        required=True,
        default="2026_1",
    )
    start_date = fields.Date(string="Fecha de inicio")
    end_date = fields.Date(string="Fecha de fin")
    weekly_hours = fields.Integer(string="Horas semanales", default=4)
    total_weeks = fields.Integer(string="Semanas", default=16)
    total_hours = fields.Integer(string="Total de horas", compute="_compute_total_hours", store=True)
    state = fields.Selection(
        [("draft", "Borrador"), ("approved", "Aprobado"), ("closed", "Cerrado")],
        string="Estado",
        default="draft",
    )
    active = fields.Boolean(string="Activo", default=True)
    objective = fields.Text(string="Objetivo")

    @api.depends("weekly_hours", "total_weeks")
    def _compute_total_hours(self):
        for plan in self:
            plan.total_hours = plan.weekly_hours * plan.total_weeks

    @api.onchange("teacher_id")
    def _onchange_teacher_id(self):
        if self.teacher_id and self.teacher_id.signature_primary:
            self.signature_id = self.teacher_id.signature_primary

    @api.constrains("weekly_hours", "total_weeks", "start_date", "end_date")
    def _check_plan_values(self):
        for plan in self:
            if plan.weekly_hours <= 0:
                raise ValidationError("Las horas semanales deben ser mayores que cero.")
            if plan.total_weeks <= 0:
                raise ValidationError("El numero de semanas debe ser mayor que cero.")
            if plan.start_date and plan.end_date and plan.end_date < plan.start_date:
                raise ValidationError("La fecha de fin no puede ser anterior a la fecha de inicio.")
