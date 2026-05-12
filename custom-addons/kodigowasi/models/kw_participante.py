from odoo import models, fields, api
from odoo.exceptions import ValidationError
from ..shared.result import UnwrapError, from_exception
import re


class KWParticipante(models.Model):
    _name = 'kw.participante'
    _description = 'Participante'

    name = fields.Char(string='Nombre completo', required=True)
    email = fields.Char(string='Correo electrónico')
    telefono = fields.Char(string='Teléfono')
    github_usuario = fields.Char(string='Usuario de GitHub')
    nivel_actual = fields.Selection([
        ('wawa', 'Wawa'),
        ('mashi', 'Mashi'),
        ('yachak', 'Yachak'),
    ], string='Nivel actual', default='wawa')
    fecha_nacimiento = fields.Date(string='Fecha de nacimiento')
    inscripcion_ids = fields.One2many('kw.inscripcion', 'participante_id', string='Inscripciones')
    activo = fields.Boolean(string='Activo', default=True)

    @api.constrains('email')
    def _check_email(self):
        for rec in self:
            if rec.email:
                # Usamos from_exception para capturar error de validación como Err
                def validate():
                    if not re.match(r"[^@]+@[^@]+\.[^@]+", rec.email or ""):
                        raise ValueError("Formato de correo inválido")
                    return None
                resultado = from_exception(validate, ValueError)
                try:
                    resultado.unwrap()
                except UnwrapError as e:
                    raise ValidationError(str(e))