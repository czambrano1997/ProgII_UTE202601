from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

STATE_LIST = [
    ('draft', 'Borrador'),
    ('pending', 'Pendiente'),
    ('approved', 'Aprobada'),
    ('rejected', 'Rechazada'),
    ('completed', 'Completada'),
]

class PatitasUnidasSolicitudAdopcion(models.Model):
    _name = 'patitas.unidas.solicitud_adopcion'
    _description = 'Solicitud de Adopción'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'request_date desc'

    name = fields.Char(string='Referencia', required=True, index=True, tracking=True, default='Nuevo')
    adopter_id = fields.Many2one('patitas.unidas.adoptante', string='Adoptante', required=True, index=True, tracking=True, ondelete='restrict')
    pet_id = fields.Many2one('patitas.unidas.mascota', string='Mascota', required=True, index=True, tracking=True, ondelete='restrict')
    request_date = fields.Date(string='Fecha de Solicitud', default=fields.Date.today, required=True, index=True)
    state = fields.Selection(STATE_LIST, string='Estado', default='draft', required=True, tracking=True, index=True)
    comments = fields.Text(string='Comentarios')

    days_elapsed = fields.Integer(
        string='Días Transcurridos', compute='_compute_days_elapsed', store=True
    )

    @api.depends('request_date')
    def _compute_days_elapsed(self):
        today = fields.Date.today()
        for record in self:
            if record.request_date:
                record.days_elapsed = (today - record.request_date).days
            else:
                record.days_elapsed = 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code('patitas.unidas.solicitud_adopcion') or 'Nuevo'
        return super().create(vals_list)

    @api.onchange('pet_id')
    def _onchange_pet_id(self):
        if not self.pet_id:
            return
        if self.pet_id.state != 'available':
            return {'warning': {
                'title': _('Mascota No Disponible'),
                'message': _('La mascota "%s" está en estado: %s. Solo se pueden adoptar mascotas disponibles.') % (
                    self.pet_id.name,
                    dict(self.pet_id._fields['state'].selection).get(self.pet_id.state)
                )
            }}
        self.state = 'pending'

    @api.onchange('adopter_id')
    def _onchange_adopter_id(self):
        if not self.adopter_id:
            return
        existing = self.search_count([
            ('adopter_id', '=', self.adopter_id.id),
            ('state', 'in', ('draft', 'pending', 'approved')),
            ('id', '!=', self.id)
        ])
        if existing > 0:
            return {'warning': {
                'title': _('Solicitud Existente'),
                'message': _('Este adoptante ya tiene %d solicitud(es) activa(s).') % existing
            }}

    @api.constrains('pet_id', 'adopter_id', 'state')
    def _check_duplicate_pending_request(self):
        for record in self:
            if record.state in ('draft', 'pending', 'approved'):
                duplicates = self.search_count([
                    ('adopter_id', '=', record.adopter_id.id),
                    ('pet_id', '=', record.pet_id.id),
                    ('state', 'in', ('draft', 'pending', 'approved')),
                    ('id', '!=', record.id)
                ])
                if duplicates > 0:
                    raise ValidationError(_('Ya existe una solicitud activa para esta combinación.'))

    def action_confirm(self):
        for record in self:
            if record.state != 'draft':
                raise UserError(_('Solo se pueden confirmar solicitudes en estado Borrador.'))
            record.state = 'pending'

    def action_approve(self):
        for record in self:
            if record.state != 'pending':
                raise UserError(_('Solo se pueden aprobar solicitudes en estado Pendiente.'))
            record.state = 'approved'

    def action_reject(self):
        for record in self:
            if record.state not in ('pending', 'approved'):
                raise UserError(_('Solo se pueden rechazar solicitudes en estado Pendiente o Aprobada.'))
            record.state = 'rejected'

    def action_complete(self):
        for record in self:
            if record.state != 'approved':
                raise UserError(_('Solo se pueden completar solicitudes en estado Aprobada.'))
            record.state = 'completed'
            if record.pet_id:
                record.pet_id.state = 'adopted'

    def action_reset_draft(self):
        for record in self:
            if record.state != 'rejected':
                raise UserError(_('Solo se pueden revertir solicitudes en estado Rechazada.'))
            record.state = 'draft'
