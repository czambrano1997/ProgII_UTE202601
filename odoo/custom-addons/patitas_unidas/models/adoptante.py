from odoo import models, fields, api, _

class PatitasUnidasAdoptante(models.Model):
    _name = 'patitas.unidas.adoptante'
    _description = 'Adoptante Potencial'
    _rec_name = 'name'
    _order = 'name asc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nombre Completo', required=True, index=True, tracking=True)
    email = fields.Char(string='Correo Electrónico', required=True, index=True, tracking=True)
    phone = fields.Char(string='Teléfono', tracking=True)
    address = fields.Text(string='Dirección')

    adoption_requests_ids = fields.One2many('patitas.unidas.solicitud_adopcion', 'adopter_id', string='Solicitudes de Adopción')

    total_requests = fields.Integer(
        string='Total Solicitudes', compute='_compute_request_stats', store=True, index=True
    )
    active_requests = fields.Integer(
        string='Solicitudes Activas', compute='_compute_request_stats', store=True
    )

    @api.depends('adoption_requests_ids', 'adoption_requests_ids.state')
    def _compute_request_stats(self):
        for record in self:
            record.total_requests = len(record.adoption_requests_ids)
            record.active_requests = len(record.adoption_requests_ids.filtered(
                lambda r: r.state in ('draft', 'pending', 'approved')
            ))

    _sql_constraints = [
        ('adoptante_email_unique', 'unique(email)', 'El correo electrónico del adoptante debe ser único.')
    ]
