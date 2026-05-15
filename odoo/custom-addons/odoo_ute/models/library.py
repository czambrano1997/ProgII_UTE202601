from odoo import models,fields,api

class library(models.Model):

    _name = 'library.ute'
    _descrition = 'library.ute'

    
    name = fields.Char(
        string='Nombre del libro',
    )
    
    
    author = fields.Char(
        string='Autor',
    )
    
    headquarters = fields.Selection(
        string='Sede',
        selection=[('South', 'Sur'), ('north', 'Norte')]
    )
   
    hous  = fields.Char(
        string='Editoria',
    )
    
    gender  = fields.Char(
        string='Genero del libro',
    )
    

    income  = fields.Date(
        string='Ingreso',
    )
    