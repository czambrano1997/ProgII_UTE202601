# Aqui se crea el modelo de lo estudiantes 
from odoo import model,fields,api

class students(model.Model):
    
    _name : 'students.ute'
    _description : 'students.ute'

    names = fields.Char(
        string='Nombres',
    )

    surnames = fields.Char(
        string='Apellidos',
    )
    
    age = fields.Integer(
        string='Edad',
    )
    
    phone = fields.Integer(
        string='telefono',
    )
    
    vat = fields.Char(
        string="CI/RUC", 
        size=13
    )
