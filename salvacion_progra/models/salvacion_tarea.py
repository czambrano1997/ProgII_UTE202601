# -*- coding: utf-8 -*-
from odoo import models, fields, api
import requests

class SalvacionLibro(models.Model):
    _name = 'salvacion.libro'
    _description = 'Gestión de Libros Biblioteca'

    name = fields.Char(string='Título del Libro', required=True)
    autor = fields.Char(string='Autor')
    codigo = fields.Char(string='Código/ISBN')
    paginas = fields.Integer(string='Número de Páginas')
    disponible = fields.Boolean(string='Disponible para Préstamo', default=True)

    @api.onchange('codigo')
    def _onchange_codigo_isbn(self):
        if self.codigo:
            isbn = self.codigo.strip().replace('-', '')
            url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json"
            
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    key = f"ISBN:{isbn}"
                    
                    if key in data:
                        libro_info = data[key]
                        self.name = libro_info.get('title', 'Sin título')
                        
                        autores = libro_info.get('authors', [])
                        if autores:
                            self.autor = autores[0].get('name', 'Autor Desconocido')
                        else:
                            self.autor = 'Autor Desconocido'
                            
                        self.paginas = libro_info.get('number_of_pages', 0)
            except Exception:
                pass