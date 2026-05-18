from odoo import api, fields, models
from odoo.exceptions import ValidationError


class JJMatricula(models.Model):
    _name = "jj.matricula"
    _description = "Matricula academica"
    _order = "registration_date desc, name"

    name = fields.Char(string="Referencia", required=True, default="Nueva matricula")
    student_id = fields.Many2one("jj.estudiante", string="Estudiante", required=True)
    subject_id = fields.Many2one("jj.asignatura", string="Asignatura", required=True)
    registration_date = fields.Date(string="Fecha de matricula", default=fields.Date.context_today)
    period = fields.Selection(
        [
            ("2026_1", "2026 - Primer periodo"),
            ("2026_2", "2026 - Segundo periodo"),
            ("2027_1", "2027 - Primer periodo"),
        ],
        string="Periodo",
        default="2026_1",
        required=True,
    )
    amount = fields.Float(string="Valor de matricula")
    paid = fields.Boolean(string="Pagado")
    first_grade = fields.Float(string="Nota 1")
    second_grade = fields.Float(string="Nota 2")
    final_grade = fields.Float(string="Nota final", compute="_compute_final_grade", store=True)
    approved = fields.Boolean(string="Aprobado", compute="_compute_final_grade", store=True)
    state = fields.Selection(
        [
            ("draft", "Borrador"),
            ("confirmed", "Confirmada"),
            ("cancelled", "Cancelada"),
        ],
        string="Estado",
        default="draft",
    )
    observations = fields.Text(string="Observaciones")

    @api.depends("first_grade", "second_grade")
    def _compute_final_grade(self):
        for record in self:
            record.final_grade = (record.first_grade + record.second_grade) / 2
            record.approved = record.final_grade >= 7

    @api.onchange("subject_id")
    def _onchange_subject_id(self):
        if self.subject_id:
            self.amount = self.subject_id.credits * 25.0
            if self.student_id:
                self.name = "%s - %s" % (self.student_id.name, self.subject_id.name)

    @api.constrains("first_grade", "second_grade", "amount")
    def _check_registration_values(self):
        for record in self:
            if record.first_grade < 0 or record.first_grade > 10:
                raise ValidationError("La nota 1 debe estar entre 0 y 10.")
            if record.second_grade < 0 or record.second_grade > 10:
                raise ValidationError("La nota 2 debe estar entre 0 y 10.")
            if record.amount < 0:
                raise ValidationError("El valor de matricula no puede ser negativo.")
