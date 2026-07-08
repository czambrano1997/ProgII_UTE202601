from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSignature(TransactionCase):
    """Pruebas unitarias sobre el modelo ou.signature (materias)."""

    def test_creacion_basica(self):
        materia = self.env['ou.signature'].create({'name': 'Álgebra Lineal'})
        self.assertEqual(materia.name, 'Álgebra Lineal')

    def test_varias_materias_son_independientes(self):
        m1 = self.env['ou.signature'].create({'name': 'Cálculo I'})
        m2 = self.env['ou.signature'].create({'name': 'Cálculo II'})
        self.assertNotEqual(m1.id, m2.id)
