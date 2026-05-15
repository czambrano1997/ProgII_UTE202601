from odoo import models,fields,api

class book_loan(models.Model):
    _name = 'book_loan.ute'
    _description = 'book_loan.ute'

    
    name = fields.Many2one(
        string='Estudiante',
        comodel_name='students.ute',
    )
    
    book  = fields.Many2one(
        string='Nombre del libro',
        comodel_name='library.ute',
        
    )
    
    book_gender =  fields.Char(
        string='Genero',
        related='book.gender',
    )
    
    loan_date = fields.Date(
        string='Fecha de prestamo',
        default=fields.Date.context_today,
    )
    