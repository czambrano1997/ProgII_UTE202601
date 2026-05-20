from odoo import models, fields, api
from datetime import datetime, timedelta

class UniversidadPersona(models.AbstractModel):
    _name = 'universidad.persona'
    _description = 'Persona (Modelo Abstracto)'
    name = fields.Char(string='Nombre Completo', required=True, help='Nombre completo de la persona')
    cedula = fields.Char(string='Cédula de Identidad', required=True, help='Número de identificación único')
    correo = fields.Char(string='Correo Electrónico', required=True, help='Correo electrónico válido')
    telefono = fields.Char(string='Teléfono', help='Número telefónico de contacto')
    direccion = fields.Text(string='Dirección', help='Dirección física completa')
    fecha_nacimiento = fields.Date(string='Fecha de Nacimiento', required=True, help='Fecha de nacimiento de la persona')
    activo = fields.Boolean(string='Activo', default=True, help='Indica si la persona está activa en el sistema')
    edad = fields.Integer(string='Edad', compute='_compute_edad', store=False, help='Edad calculada desde fecha de nacimiento')
    foto = fields.Binary(string='Foto de Perfil', help='Foto de identificación')
    genero = fields.Selection([('masculino', 'Masculino'), ('femenino', 'Femenino'), ('otro', 'Otro')], string='Género', help='Género de la persona')

    @api.depends('fecha_nacimiento')
    def _compute_edad(self):
        for record in self:
            if record.fecha_nacimiento:
                today = fields.Date.today()
                edad = today.year - record.fecha_nacimiento.year
                if (today.month, today.day) < (record.fecha_nacimiento.month, record.fecha_nacimiento.day):
                    edad -= 1
                record.edad = edad
            else:
                record.edad = 0

    @api.constrains('cedula')
    def _validar_cedula(self):
        for record in self:
            if not record.cedula or len(record.cedula) < 5:
                raise models.ValidationError('La cédula debe tener al menos 5 caracteres')
            if not record.cedula.replace('-', '').isalnum():
                raise models.ValidationError('La cédula solo puede contener números y guiones')

    @api.constrains('correo')
    def _validar_correo(self):
        for record in self:
            if record.correo and '@' not in record.correo:
                raise models.ValidationError('El correo electrónico debe contener el símbolo @')

    @api.constrains('fecha_nacimiento')
    def _validar_fecha_nacimiento(self):
        for record in self:
            if record.fecha_nacimiento:
                today = fields.Date.today()
                if record.fecha_nacimiento > today:
                    raise models.ValidationError('La fecha de nacimiento no puede ser posterior a hoy')
            if record.edad < 18:
                raise models.ValidationError('La persona debe ser mayor de 18 años')

    @api.onchange('name')
    def _onchange_name(self):
        if self.name and (not self.correo):
            nombre_limpio = self.name.lower().replace(' ', '.')
            self.correo = f'{nombre_limpio}@universidad.edu.ec'

    @api.onchange('fecha_nacimiento')
    def _onchange_fecha_nacimiento(self):
        if self.fecha_nacimiento:
            today = fields.Date.today()
            self.edad = today.year - self.fecha_nacimiento.year

    def obtener_descripcion(self):
        return f'Persona: {self.name} ({self.cedula})'

    def obtener_datos_contacto(self):
        return {'nombre': self.name, 'correo': self.correo, 'telefono': self.telefono, 'direccion': self.direccion}

    def puede_ingresar_sistema(self):
        if not self.activo:
            return False
        if self.edad < 18:
            return False
        return True

    def search_por_cedula(self, cedula):
        return self.search([('cedula', '=', cedula)], limit=1)

    def search_por_correo(self, correo):
        return self.search([('correo', '=', correo)], limit=1)
