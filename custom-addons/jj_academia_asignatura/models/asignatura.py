from odoo import api, fields, models
from odoo.exceptions import ValidationError


class JJAsignatura(models.Model):
    _name = "jj.asignatura"
    _description = "Asignatura"
    _order = "name"

    name = fields.Char(string="Nombre", required=True)
    code = fields.Char(string="Codigo", required=True)
    career_id = fields.Many2one("jj.carrera", string="Carrera", required=True)
    teacher_id = fields.Many2one("jj.docente", string="Docente")
    credits = fields.Integer(string="Creditos", default=3)
    weekly_hours = fields.Integer(string="Horas semanales", default=4)
    classroom_capacity = fields.Integer(string="Cupo", default=30)
    level = fields.Selection(
        [
            ("basica", "Basica"),
            ("intermedia", "Intermedia"),
            ("avanzada", "Avanzada"),
        ],
        string="Nivel",
        default="basica",
    )
    is_virtual = fields.Boolean(string="Es virtual")
    teacher_hourly_rate = fields.Float(
        string="Valor hora docente",
        related="teacher_id.hourly_rate",
        readonly=True,
    )
    estimated_monthly_cost = fields.Float(
        string="Costo mensual estimado",
        compute="_compute_estimated_monthly_cost",
        store=True,
    )
    description = fields.Text(string="Descripcion")

    _sql_constraints = [
        ("code_unique", "unique(code)", "El codigo de la asignatura debe ser unico."),
    ]

    @api.depends("weekly_hours", "teacher_id.hourly_rate")
    def _compute_estimated_monthly_cost(self):
        for record in self:
            record.estimated_monthly_cost = record.weekly_hours * 4 * (record.teacher_id.hourly_rate or 0.0)

    @api.onchange("is_virtual")
    def _onchange_is_virtual(self):
        if self.is_virtual:
            self.classroom_capacity = 80
        elif not self.classroom_capacity or self.classroom_capacity > 50:
            self.classroom_capacity = 30

    @api.constrains("credits", "weekly_hours", "classroom_capacity")
    def _check_subject_values(self):
        for record in self:
            if record.credits <= 0:
                raise ValidationError("Los creditos deben ser mayores que cero.")
            if record.weekly_hours <= 0:
                raise ValidationError("Las horas semanales deben ser mayores que cero.")
            if record.classroom_capacity <= 0:
                raise ValidationError("El cupo debe ser mayor que cero.")
