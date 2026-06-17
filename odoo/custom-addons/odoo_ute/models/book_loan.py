from odoo import models,fields,api

class book_loan(models.Model):
    _name = 'book_loan.ute'
    _description = 'book_loan.ute'

    
    name = fields.Many2one(
        string='Estudiante',
        comodel_name='students.ute',
        required=True
    )
    
    book  = fields.Many2one(
        string='Nombre del libro',
        comodel_name='library.ute',
        required=True
        
    )
    
    book_gender =  fields.Char(
        string='Genero',
        related='book.gender',
        required=True
    )
    
    loan_date = fields.Date(
        string='Fecha de prestamo',
        default=fields.Date.context_today,
        required=True
    )

    book_observations = fields.Text(
        string='Observaciones',
    )
    
    