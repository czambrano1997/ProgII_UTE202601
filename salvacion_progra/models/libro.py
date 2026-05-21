# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import requests
import base64

# --- NUEVO MODELO: SEDES / UBICACIONES FÍSICAS ---
class BibliotecaSede(models.Model):
    _name = 'biblioteca.sede'
    _description = 'Sedes y Salas de la Biblioteca UTE'

    name = fields.Char(string='Nombre de la Sede / Sala', required=True)
    ubicacion = fields.Char(string='Ubicación / Campus')
    responsable = fields.Char(string='Responsable de Sala')
    
    # Permite ver qué libros están asignados a esta sede en específico
    libro_ids = fields.One2many('biblioteca.libro', 'sede_id', string='Libros en esta Sede')

class BibliotecaEstudiante(models.Model):
    _name = 'biblioteca.estudiante'
    _description = 'Registro de Estudiantes / Lectores UTE'
    _rec_name = 'name'

    name = fields.Char(string='Nombre Completo', required=True)
    matricula = fields.Char(string='Número de Matrícula / Cédula', required=True)
    correo = fields.Char(string='Correo Institucional')
    carrera = fields.Selection([
        ('software', 'Desarrollo de Software'),
        ('automotriz', 'Ingeniería Automotriz'),
        ('ciberseguridad', 'Ciberseguridad'),
        ('redes', 'Telecomunicaciones / Redes')
    ], string='Carrera', default='software')
    
    prestamo_ids = fields.One2many('biblioteca.prestamo', 'estudiante_id', string='Historial de Préstamos')
    multa_ids = fields.One2many('biblioteca.multa', 'estudiante_id', string='Historial de Sanciones')

class BibliotecaAutor(models.Model):
    _name = 'biblioteca.autor'
    _description = 'Autores de Libros'

    name = fields.Char(string='Nombre del Autor', required=True)
    biografia = fields.Text(string='Biografía Breve')

class BibliotecaLibro(models.Model):
    _name = 'biblioteca.libro'
    _description = 'Gestión de Libros - Biblioteca UTE'

    name = fields.Char(string='Título del Libro', required=True)
    autor_id = fields.Many2one('biblioteca.autor', string='Autor', required=True)
    codigo = fields.Char(string='Código / ISBN', required=True)
    paginas = fields.Integer(string='Número de Páginas')
    disponible = fields.Boolean(string='Disponible para Préstamo', default=True)
    editorial = fields.Char(string='Editorial')
    fecha_publicacion = fields.Char(string='Año de Publicación')
    resumen = fields.Text(string='Sinopsis / Resumen del Libro')
    imagen = fields.Binary(string='Portada del Libro')
    
    # --- RELACIÓN CON LA NUEVA TABLA DE SEDES ---
    sede_id = fields.Many2one('biblioteca.sede', string='Sede / Ubicación Física')

    @api.onchange('codigo')
    def _onchange_codigo_isbn(self):
        if self.codigo:
            isbn = self.codigo.strip().replace('-', '')
            url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json"
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    key = f"ISBN:{isbn}"
                    if key in data:
                        libro_info = data[key]
                        self.name = libro_info.get('title', 'Sin título')
                        self.paginas = libro_info.get('number_of_pages', 0)
                        self.fecha_publicacion = libro_info.get('publish_date', '')
                        editoriales = libro_info.get('publishers', [])
                        if editoriales:
                            self.editorial = editoriales[0].get('name', '')
                        
                        url_imagen = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
                        res_img = requests.get(url_imagen, timeout=10)
                        if res_img.status_code == 200 and len(res_img.content) > 100:
                            self.imagen = base64.b64encode(res_img.content)
                        else:
                            self.imagen = False
                        
                        autores_api = libro_info.get('authors', [])
                        nombre_autor = autores_api[0].get('name', 'Autor Desconocido') if autores_api else 'Autor Desconocido'
                        autor_existente = self.env['biblioteca.autor'].search([('name', '=', nombre_autor)], limit=1)
                        if autor_existente:
                            self.autor_id = autor_existente.id
                        else:
                            self.autor_id = self.env['biblioteca.autor'].create({'name': nombre_autor}).id
            except Exception:
                pass

class BibliotecaPrestamo(models.Model):
    _name = 'biblioteca.prestamo'
    _description = 'Registro de Préstamos'
    _order = 'fecha_prestamo desc'

    libro_id = fields.Many2one('biblioteca.libro', string='Libro a Prestar', required=True, domain=[('disponible', '=', True)])
    estudiante_id = fields.Many2one('biblioteca.estudiante', string='Estudiante / Lector', required=True)
    fecha_prestamo = fields.Date(string='Fecha de Salida', default=fields.Date.context_today, required=True)
    fecha_devolucion = fields.Date(string='Fecha Límite Devolución', required=True)
    estado = fields.Selection([
        ('prestado', 'En Préstamo'),
        ('devuelto', 'Devuelto a Tiempo'),
        ('atrasado', 'Atrasado')
    ], string='Estado del Préstamo', default='prestado', required=True)

    @api.constrains('estudiante_id', 'estado')
    def _check_multas_pendientes(self):
        for prestamo in self:
            if prestamo.estado in ['prestado', 'atrasado'] and prestamo.estudiante_id:
                multas_deudoras = self.env['biblioteca.multa'].search([
                    ('estudiante_id', '=', prestamo.estudiante_id.id),
                    ('estado_pago', '=', 'pendiente')
                ])
                if multas_deudoras:
                    total_deuda = sum(m.monto for m in multas_deudoras)
                    raise ValidationError(
                        f"¡PRÉSTAMO DENEGADO!\n\n"
                        f"El estudiante '{prestamo.estudiante_id.name}' registra multas pendientes por un valor total de ${total_deuda:.2f}.\n"
                        f"Debe cancelar sus saldos en el apartado de Multas antes de solicitar otro libro."
                    )

    @api.model_create_multi
    def create(self, vals_list):
        prestamos = super(BibliotecaPrestamo, self).create(vals_list)
        for prestamo in prestamos:
            if prestamo.estado in ['prestado', 'atrasado']:
                prestamo.libro_id.disponible = False
            if prestamo.estado == 'atrasado':
                prestamo._generar_multa_automatica()
        return prestamos

    def write(self, vals):
        res = super(BibliotecaPrestamo, self).write(vals)
        if 'estado' in vals:
            for prestamo in self:
                if prestamo.estado == 'devuelto':
                    prestamo.libro_id.disponible = True
                else:
                    prestamo.libro_id.disponible = False
                if prestamo.estado == 'atrasado':
                    prestamo._generar_multa_automatica()
        return res

    def _generar_multa_automatica(self):
        multa_existente = self.env['biblioteca.multa'].search([('prestamo_id', '=', self.id)], limit=1)
        if not multa_existente:
            self.env['biblioteca.multa'].create({
                'prestamo_id': self.id,
                'estudiante_id': self.estudiante_id.id,
                'monto': 5.00,
                'estado_pago': 'pendiente'
            })

class BibliotecaMulta(models.Model):
    _name = 'biblioteca.multa'
    _description = 'Control de Multas de la Biblioteca'

    prestamo_id = fields.Many2one('biblioteca.prestamo', string='Préstamo Origen', required=True, ondelete='cascade')
    estudiante_id = fields.Many2one('biblioteca.estudiante', string='Estudiante Sancionado', required=True)
    monto = fields.Float(string='Monto a Pagar ($)', default=5.00, required=True)
    fecha_multa = fields.Date(string='Fecha de Sanción', default=fields.Date.context_today, required=True)
    estado_pago = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado')
    ], string='Estado del Pago', default='pendiente', required=True)