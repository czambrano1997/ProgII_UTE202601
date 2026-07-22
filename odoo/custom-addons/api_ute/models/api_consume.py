from odoo import models, fields, api
import requests

class api_ute(models.Model):
    _name = 'ou.api.consume'
    _description = 'Consumo de APIs'

    url = fields.Char(string='Enlace')
    name = fields.Char(string='Nombre')
    status = fields.Selection([
        ('down', 'Caido'),
        ('no_response', 'Sin respuesta'),
        ('up', 'Habilitado')
    ],
    string="Status")


    def check_status(self):
        print("check_status")
        result = requests.get(self.url)
        print(result.status_code)
        print(result.json())
        dict_result = result.json()
        if result.status_code == 200 and dict_result['ok']:
            self.status = 'up'
        elif result.status_code == 200 and not dict_result['ok']:
            self.status = 'no_response'
        else:
            self.status = 'down'
