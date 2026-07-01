from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestTeacher(TransactionCase):
    """Pruebas unitarias/funcionales sobre el modelo sistema.usuarios (docentes)."""

    def setUp(self):
        super().setUp()
        self.Teacher = self.env['sistema.usuarios']

    def test_creacion_basica(self):
        docente = self.Teacher.create({
            'name': 'Ana',
            'last_name': 'Pérez',
            'email': 'ana@example.com',
        })
        self.assertEqual(docente.name, 'Ana')
        self.assertEqual(docente.last_name, 'Pérez')

    def test_email_valido_marca_validado(self):
        docente = self.Teacher.create({
            'name': 'Ana', 'last_name': 'Pérez', 'email': 'ana@example.com',
        })
        self.assertEqual(docente.validate_email, 'Validado')

    def test_email_invalido_marca_no_valido(self):
        docente = self.Teacher.create({
            'name': 'Ana', 'last_name': 'Pérez', 'email': 'ana-sin-arroba',
        })
        self.assertEqual(docente.validate_email, 'No valido')

    def test_sin_email_marca_no_valido(self):
        docente = self.Teacher.create({'name': 'Ana', 'last_name': 'Pérez'})
        self.assertEqual(docente.validate_email, 'No valido')

    def test_vat_corto_lanza_error(self):
        with self.assertRaises(ValidationError):
            self.Teacher.create({
                'name': 'Ana', 'last_name': 'Pérez', 'vat': '123',
            })

    def test_vat_valido_no_lanza_error(self):
        docente = self.Teacher.create({
            'name': 'Ana', 'last_name': 'Pérez', 'vat': '1234567890',
        })
        self.assertEqual(docente.vat, '1234567890')

    def test_relacion_m2m_signature_ids(self):
        materia = self.env['ou.signature'].create({'name': 'Programación II'})
        docente = self.Teacher.create({
            'name': 'Ana', 'last_name': 'Pérez',
            'signature_ids': [(4, materia.id)],
        })
        self.assertIn(materia, docente.signature_ids)

    def test_relacion_m2o_signature_primary(self):
        materia = self.env['ou.signature'].create({'name': 'Bases de Datos'})
        docente = self.Teacher.create({
            'name': 'Ana', 'last_name': 'Pérez',
            'signature_primary': materia.id,
        })
        self.assertEqual(docente.signature_primary, materia)
