<<<<<<< HEAD
# Aqui se crea el modelo de lo estudiantes 
from odoo import models,fields,api

class students(models.Model):
    
    _name = 'students.ute'
    _description = 'students.ute'
    

    name = fields.Char(
        string='Nombres',
    )
=======
    # Aqui se crea el modelo de lo estudiantes 
from odoo import models, fields, api

class students(models.Model):
        
        _name = 'ou.students'
        

        name = fields.Char(
            string='Nombres',
        )
>>>>>>> 4159c1e03c480c0ecec9608bc80bbb8697e392d1

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
