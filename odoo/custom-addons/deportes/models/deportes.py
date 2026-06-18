# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Deportes(models.Model):
    _name = 'deportes'
    _description = 'Deportes'

    name = fields.Char(string="Name", required=True)
    sport_type = fields.Selection(
        [
            ('futbol', 'Fútbol'),
            ('basket', 'Basket'),
            ('voley', 'Vóley'),
            ('padel', 'Padel'),
        ],
        string='Deporte',
        default='futbol',
        required=True,
    )
    state = fields.Selection(
        [('reservar', 'Reservar'), ('Reservada', 'reservada'), ('en_espera', 'En_espera')],
        default='reservar', string="Estado"
    )
    description = fields.Text(string="Description")
    amount = fields.Float(string="Amount")
    active = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override the create method to assign a sequence-generated name 
        to each record being created.

        :param vals_list: List of dictionaries with field values for new records.
        :return: Recordset of newly created records.
        """
        return super().create(vals_list)

    def write(self, vals):
        """
        Override the write method to include custom behavior when updating records.

        :param vals: Dictionary of field values to update.
        :return: True if the write was successful.
        """
        return super().write(vals)

    def unlink(self):
        """
        Override the unlink method to include custom behavior when deleting records.

        :return: True if the records were successfully deleted.
        """
        return super().unlink()

    def action_do_something(self):
        self.ensure_one()
        # Placeholder for button action
        pass
    