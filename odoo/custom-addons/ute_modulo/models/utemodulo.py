from odoo import models, fields 
class Estudiantes(models.Model): 
    _name = "mode_ute.estudiantes" # <-- debe coincidir exacto _description = "Estudiantes UTE" 
    name = fields.Char("Nombre", required=True) 
    age = fields.Integer("Edad")
