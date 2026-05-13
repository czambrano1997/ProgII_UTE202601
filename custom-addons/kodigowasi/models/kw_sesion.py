from odoo import models, fields, api


class KWSesion(models.Model):
    _name = 'kw.sesion'
    _description = 'Sesión de Taller'

    name = fields.Char(string='Título', required=True)
    taller_id = fields.Many2one('kw.taller', string='Taller', required=True, ondelete='cascade')
    fecha_hora = fields.Datetime(string='Fecha y hora')
    duracion_minutos = fields.Integer(string='Duración (min)')
    contenido = fields.Html(string='Contenido')
    link_meet = fields.Char(string='Enlace de reunión')
    completada = fields.Boolean(string='Completada', default=False)

    @api.onchange('taller_id')
    def _onchange_taller(self):
        if self.taller_id and self.taller_id.fecha_inicio:
            # Sugiere la fecha del taller por defecto, si no está puesta
            self.fecha_hora = fields.Datetime.to_datetime(self.taller_id.fecha_inicio)