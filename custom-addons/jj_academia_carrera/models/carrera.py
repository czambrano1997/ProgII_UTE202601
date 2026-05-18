from odoo import api, fields, models
from odoo.exceptions import ValidationError


class JJCarrera(models.Model):
    _name = "jj.carrera"
    _description = "Carrera academica"
    _order = "name"

    name = fields.Char(string="Nombre", required=True)
    code = fields.Char(string="Codigo", required=True)
    active = fields.Boolean(string="Activa", default=True)
    modality = fields.Selection(
        [
            ("presencial", "Presencial"),
            ("virtual", "Virtual"),
            ("hibrida", "Hibrida"),
        ],
        string="Modalidad",
        default="presencial",
        required=True,
    )
    duration_semesters = fields.Integer(string="Duracion en semestres", default=8)
    monthly_fee = fields.Float(string="Mensualidad", default=120.0)
    start_date = fields.Date(string="Fecha de inicio")
    coordinator_id = fields.Many2one("res.partner", string="Coordinador")
    description = fields.Text(string="Descripcion")
    total_estimated_cost = fields.Float(
        string="Costo estimado total",
        compute="_compute_total_estimated_cost",
        store=True,
    )

    _sql_constraints = [
        ("code_unique", "unique(code)", "El codigo de la carrera debe ser unico."),
    ]

    @api.depends("duration_semesters", "monthly_fee")
    def _compute_total_estimated_cost(self):
        for record in self:
            record.total_estimated_cost = record.duration_semesters * 6 * record.monthly_fee

    @api.onchange("modality")
    def _onchange_modality(self):
        if self.modality == "virtual":
            self.monthly_fee = 90.0
        elif self.modality == "hibrida":
            self.monthly_fee = 110.0
        elif self.modality == "presencial":
            self.monthly_fee = 120.0

    @api.constrains("duration_semesters", "monthly_fee", "code")
    def _check_academic_values(self):
        for record in self:
            if record.duration_semesters <= 0:
                raise ValidationError("La duracion debe ser mayor que cero.")
            if record.monthly_fee < 0:
                raise ValidationError("La mensualidad no puede ser negativa.")
            if record.code and len(record.code.strip()) < 3:
                raise ValidationError("El codigo debe tener al menos 3 caracteres.")
