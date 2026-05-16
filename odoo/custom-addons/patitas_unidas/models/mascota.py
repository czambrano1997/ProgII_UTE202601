from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

SPECIES_LIST = [
    ('dog', 'Perro'),
    ('cat', 'Gato'),
    ('bird', 'Ave'),
    ('other', 'Otro'),
]

STATE_LIST = [
    ('available', 'Disponible'),
    ('in_foster', 'En acogida'),
    ('in_adoption_process', 'En proceso de adopción'),
    ('adopted', 'Adoptada'),
    ('deceased', 'Fallecida'),
]

class PatitasUnidasMascota(models.Model):
    _name = 'patitas.unidas.mascota'
    _description = 'Mascota en el sistema Patitas Unidas'
    _rec_name = 'name'
    _order = 'name asc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nombre', required=True, index=True, tracking=True)
    species = fields.Selection(SPECIES_LIST, string='Especie', required=True, tracking=True)
    breed = fields.Char(string='Raza', tracking=True)
    age_months = fields.Integer(string='Edad (meses)', default=0)
    state = fields.Selection(STATE_LIST, string='Estado', default='available', required=True, tracking=True, index=True)
    foster_home_id = fields.Many2one('patitas.unidas.hogar_adoptivo', string='Hogar Adoptivo', index=True, tracking=True, ondelete='restrict')

    medical_history_ids = fields.One2many('patitas.unidas.historial_medico', 'pet_id', string='Historial Médico')
    adoption_requests_ids = fields.One2many('patitas.unidas.solicitud_adopcion', 'pet_id', string='Solicitudes de Adopción')

    medical_records_count = fields.Integer(
        string='Nº Registros Médicos',
        compute='_compute_medical_records_count',
        store=True,
        index=True
    )

    @api.depends('medical_history_ids')
    def _compute_medical_records_count(self):
        for record in self:
            record.medical_records_count = len(record.medical_history_ids)

    @api.onchange('foster_home_id')
    def _onchange_foster_home_id(self):
        if not self.foster_home_id:
            if self.state == 'in_foster':
                self.state = 'available'
            return

        if not self.foster_home_id.active:
            return {'warning': {
                'title': _('Hogar Inactivo'),
                'message': _('El hogar seleccionado no está activo. Selecciona otro o actívalo primero.')
            }}

        occupancy = len(self.foster_home_id.pets_ids)
        if occupancy >= self.foster_home_id.max_capacity:
            return {'warning': {
                'title': _('Capacidad Excedida'),
                'message': _('El hogar ya tiene %d/%d mascotas. No puede alojar más.') % (occupancy, self.foster_home_id.max_capacity)
            }}

        self.state = 'in_foster'
