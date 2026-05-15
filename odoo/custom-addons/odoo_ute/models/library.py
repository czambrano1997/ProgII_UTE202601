from odoo import models,fields,api

class library(models.Model):

    _name = 'library.ute'
    _descrition = 'library.ute'

    
    name = fields.Char(
        string='Nombre del libro',
        required=True
    )
    
    
    author = fields.Char(
        string='Autor',
        required=True
    )
    
    headquarters = fields.Selection(
        string='Sede',
        selection=[('South', 'Sur'), ('north', 'Norte')],
        required=True
    )
   
    hous  = fields.Char(
        string='Editoria',
        required=True
    )
    
    gender  = fields.Char(
        string='Genero del libro',
        required=True
    )
    

    income  = fields.Date(
        string='Ingreso',
        required=True
    )
    