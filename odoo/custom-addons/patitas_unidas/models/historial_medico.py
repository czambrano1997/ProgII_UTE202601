from odoo import models, fields, api, _
from odoo.exceptions import UserError

CARE_TYPE_LIST = [
    ('vaccination', 'Vacunación'),
    ('checkup', 'Chequeo general'),
    ('surgery', 'Cirugía'),
    ('treatment', 'Tratamiento'),
    ('other', 'Otro'),
]

class PatitasUnidasHistorialMedico(models.Model):
    _name = 'patitas.unidas.historial_medico'
    _description = 'Historial Médico de Mascota'
    _rec_name = 'pet_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    pet_id = fields.Many2one('patitas.unidas.mascota', string='Mascota', required=True, index=True, ondelete='cascade', tracking=True)
    date = fields.Date(string='Fecha', required=True, default=fields.Date.today, index=True, tracking=True)
    care_type = fields.Selection(CARE_TYPE_LIST, string='Tipo de Atención', required=True, tracking=True)
    description = fields.Text(string='Descripción')
    veterinarian = fields.Char(string='Veterinario', tracking=True)

    @api.onchange('date')
    def _onchange_date(self):
        if self.date and self.date > fields.Date.today():
            return {'warning': {
                'title': _('Fecha Futura'),
                'message': _('No es posible registrar atenciones con fecha futura.')
            }}

    @api.onchange('care_type')
    def _onchange_care_type(self):
        templates = {
            'vaccination': 'Aplicación de vacuna: ',
            'checkup': 'Chequeo general: ',
            'surgery': 'Intervención quirúrgica: ',
            'treatment': 'Tratamiento médico: ',
            'other': 'Detalle: '
        }
        if self.care_type and not self.description:
            self.description = templates.get(self.care_type, '')
