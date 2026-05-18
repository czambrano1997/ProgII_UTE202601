from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Classroom(models.Model):
    _name = "ou.classroom"
    _description = "Aula UTE"
    _order = "code"

    name = fields.Char(string="Nombre", required=True)
    code = fields.Char(string="Codigo", required=True)
    building = fields.Char(string="Edificio")
    floor = fields.Integer(string="Piso")
    capacity = fields.Integer(string="Capacidad", default=30)
    room_type = fields.Selection(
        [
            ("normal", "Aula normal"),
            ("laboratory", "Laboratorio"),
            ("auditorium", "Auditorio"),
            ("virtual", "Virtual"),
        ],
        string="Tipo",
        default="normal",
        required=True,
    )
    has_projector = fields.Boolean(string="Tiene proyector")
    has_computers = fields.Boolean(string="Tiene computadores")
    active = fields.Boolean(string="Activa", default=True)
    display_label = fields.Char(string="Etiqueta", compute="_compute_display_label", store=True)
    notes = fields.Text(string="Observaciones")

    _code_unique = models.Constraint(
        "unique(code)",
        "El codigo del aula debe ser unico.",
    )

    @api.depends("code", "name", "building")
    def _compute_display_label(self):
        for classroom in self:
            parts = [classroom.code or "", classroom.name or "", classroom.building or ""]
            classroom.display_label = " - ".join([part for part in parts if part])

    @api.onchange("room_type")
    def _onchange_room_type(self):
        if self.room_type == "laboratory":
            self.has_computers = True
            self.has_projector = True
        elif self.room_type == "virtual":
            self.capacity = 100

    @api.constrains("capacity", "floor")
    def _check_classroom_values(self):
        for classroom in self:
            if classroom.capacity <= 0:
                raise ValidationError("La capacidad debe ser mayor que cero.")
            if classroom.floor < 0:
                raise ValidationError("El piso no puede ser negativo.")
