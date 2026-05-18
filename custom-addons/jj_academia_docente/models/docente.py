from odoo import api, fields, models
from odoo.exceptions import ValidationError


class JJDocente(models.Model):
    _name = "jj.docente"
    _description = "Docente"
    _order = "name"

    name = fields.Char(string="Nombre completo", required=True)
    identification = fields.Char(string="Identificacion", required=True)
    email = fields.Char(string="Correo")
    phone = fields.Char(string="Telefono")
    active = fields.Boolean(string="Activo", default=True)
    hire_date = fields.Date(string="Fecha de contratacion")
    contract_type = fields.Selection(
        [
            ("tiempo_completo", "Tiempo completo"),
            ("medio_tiempo", "Medio tiempo"),
            ("hora_clase", "Hora clase"),
        ],
        string="Tipo de contrato",
        default="hora_clase",
        required=True,
    )
    hourly_rate = fields.Float(string="Valor por hora", default=12.0)
    weekly_hours = fields.Integer(string="Horas semanales", default=10)
    monthly_salary = fields.Float(
        string="Salario mensual estimado",
        compute="_compute_monthly_salary",
        store=True,
    )
    has_master_degree = fields.Boolean(string="Tiene maestria")
    specialty = fields.Char(string="Especialidad")
    biography = fields.Text(string="Biografia")

    _sql_constraints = [
        ("identification_unique", "unique(identification)", "La identificacion del docente debe ser unica."),
    ]

    @api.depends("hourly_rate", "weekly_hours")
    def _compute_monthly_salary(self):
        for record in self:
            record.monthly_salary = record.hourly_rate * record.weekly_hours * 4

    @api.onchange("contract_type")
    def _onchange_contract_type(self):
        if self.contract_type == "tiempo_completo":
            self.weekly_hours = 40
            self.hourly_rate = 15.0
        elif self.contract_type == "medio_tiempo":
            self.weekly_hours = 20
            self.hourly_rate = 13.0
        elif self.contract_type == "hora_clase":
            self.weekly_hours = 10
            self.hourly_rate = 12.0

    @api.constrains("hourly_rate", "weekly_hours")
    def _check_teacher_values(self):
        for record in self:
            if record.hourly_rate <= 0:
                raise ValidationError("El valor por hora debe ser mayor que cero.")
            if record.weekly_hours <= 0 or record.weekly_hours > 40:
                raise ValidationError("Las horas semanales deben estar entre 1 y 40.")
