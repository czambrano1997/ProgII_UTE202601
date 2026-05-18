from odoo import api, fields, models
from odoo.exceptions import ValidationError


class JJEstudiante(models.Model):
    _name = "jj.estudiante"
    _description = "Estudiante"
    _order = "name"

    name = fields.Char(string="Nombre completo", required=True)
    document = fields.Char(string="Cedula o documento", required=True)
    age = fields.Integer(string="Edad")
    email = fields.Char(string="Correo")
    phone = fields.Char(string="Telefono")
    active = fields.Boolean(string="Activo", default=True)
    enrollment_date = fields.Date(string="Fecha de ingreso", default=fields.Date.context_today)
    career_id = fields.Many2one("jj.carrera", string="Carrera", required=True)
    semester = fields.Selection(
        [(str(number), str(number)) for number in range(1, 11)],
        string="Semestre",
        default="1",
    )
    average = fields.Float(string="Promedio")
    scholarship = fields.Boolean(string="Tiene beca")
    scholarship_percent = fields.Float(string="Porcentaje de beca")
    final_monthly_fee = fields.Float(
        string="Mensualidad final",
        compute="_compute_final_monthly_fee",
        store=True,
    )
    status = fields.Selection(
        [
            ("regular", "Regular"),
            ("observacion", "En observacion"),
            ("graduado", "Graduado"),
        ],
        string="Estado",
        default="regular",
    )
    notes = fields.Text(string="Observaciones")

    _sql_constraints = [
        ("document_unique", "unique(document)", "El documento del estudiante debe ser unico."),
    ]

    @api.depends("career_id.monthly_fee", "scholarship", "scholarship_percent")
    def _compute_final_monthly_fee(self):
        for record in self:
            base_fee = record.career_id.monthly_fee or 0.0
            discount = record.scholarship_percent if record.scholarship else 0.0
            record.final_monthly_fee = base_fee * (1 - (discount / 100))

    @api.onchange("scholarship")
    def _onchange_scholarship(self):
        if not self.scholarship:
            self.scholarship_percent = 0.0
        elif not self.scholarship_percent:
            self.scholarship_percent = 25.0

    @api.constrains("age", "average", "scholarship_percent")
    def _check_student_values(self):
        for record in self:
            if record.age and record.age < 16:
                raise ValidationError("La edad minima del estudiante es 16.")
            if record.average < 0 or record.average > 10:
                raise ValidationError("El promedio debe estar entre 0 y 10.")
            if record.scholarship_percent < 0 or record.scholarship_percent > 100:
                raise ValidationError("La beca debe estar entre 0% y 100%.")
