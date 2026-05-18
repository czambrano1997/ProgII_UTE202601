from odoo import api, fields, models


class TeacherUTE(models.Model):
    _inherit = "ou.teacher"

    full_name = fields.Char(string="Nombre completo", compute="_compute_full_name", store=True)
    academic_plan_ids = fields.One2many("ou.academic.plan", "teacher_id", string="Planes academicos")
    schedule_ids = fields.One2many("ou.class.schedule", "teacher_id", string="Horarios")
    attendance_ids = fields.One2many("ou.attendance", "teacher_id", string="Asistencias")
    evaluation_ids = fields.One2many("ou.teacher.evaluation", "teacher_id", string="Evaluaciones")

    @api.depends("name", "last_name")
    def _compute_full_name(self):
        for teacher in self:
            teacher.full_name = "%s %s" % (teacher.name or "", teacher.last_name or "")
