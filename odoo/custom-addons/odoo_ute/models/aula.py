from odoo import models, fields

class Ute_Aulas(models.Model):
    _name = 'ou.aula'
    _description = 'Asignación de aula de clase '

    
    name = fields.Char(string = 'Nombre o número de aula', required = True)
    edificio = fields.Char(string = 'edificio', required = True)
    capacidad = fields.Integer(string= 'Capacidad', default= 30)