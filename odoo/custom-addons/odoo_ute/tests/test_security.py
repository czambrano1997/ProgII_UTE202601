from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSeguridad(TransactionCase):
    """Pruebas de seguridad: accesos por grupo sobre sistema.usuarios."""

    def setUp(self):
        super().setUp()
        group_user = self.env.ref('odoo_ute.group_ute_user')
        group_manager = self.env.ref('odoo_ute.group_ute_manager')

        self.usuario = self.env['res.users'].create({
            'name': 'Docente Usuario',
            'login': 'docente_usuario_test',
            'email': 'docente_usuario_test@example.com',
            'group_ids': [(6, 0, [group_user.id])],
        })
        self.manager = self.env['res.users'].create({
            'name': 'Docente Manager',
            'login': 'docente_manager_test',
            'email': 'docente_manager_test@example.com',
            'group_ids': [(6, 0, [group_manager.id])],
        })

    def test_usuario_sin_permiso_no_puede_crear(self):
        # ir.model.access.csv: el grupo 'Usuario' tiene perm_create=0 sobre sistema.usuarios
        with self.assertRaises(AccessError):
            self.env(user=self.usuario)['sistema.usuarios'].create({
                'name': 'Intento', 'last_name': 'Sin permiso',
            })

    def test_manager_si_puede_crear(self):
        # El grupo 'Administrador' tiene perm_create=1 sobre sistema.usuarios
        docente = self.env(user=self.manager)['sistema.usuarios'].create({
            'name': 'Autorizado', 'last_name': 'Con permiso',
        })
        self.assertTrue(docente.id)
