from odoo import api, fields, models
from odoo.exceptions import ValidationError


class TeacherEvaluation(models.Model):
    _name = "ou.teacher.evaluation"
    _description = "Evaluacion docente UTE"
    _order = "evaluation_date desc"

    name = fields.Char(string="Referencia", compute="_compute_name", store=True)
    teacher_id = fields.Many2one("ou.teacher", string="Docente", required=True)
    signature_id = fields.Many2one("ou.signature", string="Materia")
    evaluation_date = fields.Date(string="Fecha", default=fields.Date.context_today, required=True)
    evaluator = fields.Char(string="Evaluador")
    methodology_score = fields.Float(string="Metodologia")
    punctuality_score = fields.Float(string="Puntualidad")
    content_score = fields.Float(string="Dominio de contenidos")
    average_score = fields.Float(string="Promedio", compute="_compute_average_score", store=True)
    result = fields.Selection(
        [
            ("excellent", "Excelente"),
            ("good", "Bueno"),
            ("improve", "Por mejorar"),
        ],
        string="Resultado",
        compute="_compute_average_score",
        store=True,
    )
    approved = fields.Boolean(string="Aprobado", compute="_compute_average_score", store=True)
    comments = fields.Text(string="Comentarios")

    @api.depends("teacher_id", "evaluation_date")
    def _compute_name(self):
        for evaluation in self:
            teacher = evaluation.teacher_id.full_name or evaluation.teacher_id.name or ""
            evaluation.name = "Evaluacion %s - %s" % (teacher, evaluation.evaluation_date or "")

    @api.depends("methodology_score", "punctuality_score", "content_score")
    def _compute_average_score(self):
        for evaluation in self:
            evaluation.average_score = (
                evaluation.methodology_score + evaluation.punctuality_score + evaluation.content_score
            ) / 3
            evaluation.approved = evaluation.average_score >= 7
            if evaluation.average_score >= 9:
                evaluation.result = "excellent"
            elif evaluation.average_score >= 7:
                evaluation.result = "good"
            else:
                evaluation.result = "improve"

    @api.onchange("teacher_id")
    def _onchange_teacher_id(self):
        if self.teacher_id and self.teacher_id.signature_primary:
            self.signature_id = self.teacher_id.signature_primary

    @api.constrains("methodology_score", "punctuality_score", "content_score")
    def _check_scores(self):
        for evaluation in self:
            scores = [evaluation.methodology_score, evaluation.punctuality_score, evaluation.content_score]
            if any(score < 0 or score > 10 for score in scores):
                raise ValidationError("Las calificaciones deben estar entre 0 y 10.")
