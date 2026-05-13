"""
tests/test_taller.py
====================
Tests de integración para el modelo kw.taller.

Usa TransactionCase de Odoo → cada test corre en una transacción que
se hace rollback al finalizar. No persiste datos entre tests.

Ejecutar con:
    odoo-bin -d <db> --test-enable -i kodigowasi --stop-after-init
    # o filtrando solo este módulo:
    odoo-bin -d <db> --test-tags kodigowasi -i kodigowasi --stop-after-init
"""

from datetime import date, timedelta

from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("kodigowasi", "taller", "-at_install", "post_install")
class TestKWTallerConstraints(TransactionCase):
    """Constraints y lógica del modelo kw.taller."""

    # ------------------------------------------------------------------
    # Fixtures compartidos
    # ------------------------------------------------------------------

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Taller = cls.env["kw.taller"]
        cls.Instructor = cls.env["kw.instructor"]

    def _taller_base(self, **kwargs) -> dict:
        """Valores mínimos válidos para crear un taller."""
        manana = date.today() + timedelta(days=1)
        defaults = {
            "name": "Taller Python Test",
            "coding_level": "wawa",
            "max_cupos": 10,
            "fecha_inicio": manana,
            "fecha_fin": manana + timedelta(days=30),
            "modalidad": "virtual",
        }
        defaults.update(kwargs)
        return defaults

    # ------------------------------------------------------------------
    # Creación exitosa
    # ------------------------------------------------------------------

    def test_crear_taller_valido(self):
        taller = self.Taller.create(self._taller_base())
        self.assertEqual(taller.name, "Taller Python Test")
        self.assertEqual(taller.plazas_disponibles, 10)

    def test_crear_taller_sin_fechas(self):
        """Las fechas son opcionales; debe crearse sin constraint error."""
        taller = self.Taller.create(
            self._taller_base(fecha_inicio=False, fecha_fin=False)
        )
        self.assertTrue(taller.id)

    def test_crear_taller_con_instructor(self):
        instructor = self.Instructor.create({"name": "Instructor Test"})
        taller = self.Taller.create(self._taller_base(instructor_id=instructor.id))
        self.assertEqual(taller.instructor_id, instructor)

    def test_plazas_disponibles_inicial_igual_a_max_cupos(self):
        taller = self.Taller.create(self._taller_base(max_cupos=15))
        self.assertEqual(taller.plazas_disponibles, 15)

    # ------------------------------------------------------------------
    # Constraint: fechas
    # ------------------------------------------------------------------

    def test_err_fecha_fin_igual_a_inicio(self):
        hoy = date.today() + timedelta(days=5)
        with self.assertRaises(ValidationError):
            self.Taller.create(self._taller_base(fecha_inicio=hoy, fecha_fin=hoy))

    def test_err_fecha_fin_antes_de_inicio(self):
        inicio = date.today() + timedelta(days=10)
        fin = date.today() + timedelta(days=5)
        with self.assertRaises(ValidationError):
            self.Taller.create(self._taller_base(fecha_inicio=inicio, fecha_fin=fin))

    def test_err_editar_taller_con_fechas_invalidas(self):
        taller = self.Taller.create(self._taller_base())
        inicio = date.today() + timedelta(days=10)
        fin = date.today() + timedelta(days=5)
        with self.assertRaises(ValidationError):
            taller.write({"fecha_inicio": inicio, "fecha_fin": fin})

    def test_ok_actualizar_fechas_validas(self):
        taller = self.Taller.create(self._taller_base())
        nueva_fin = date.today() + timedelta(days=60)
        taller.write({"fecha_fin": nueva_fin})
        self.assertEqual(taller.fecha_fin, nueva_fin)

    # ------------------------------------------------------------------
    # Compute: plazas_disponibles
    # ------------------------------------------------------------------

    def test_plazas_disminuyen_con_inscripciones_confirmadas(self):
        taller = self.Taller.create(self._taller_base(max_cupos=5))
        Participante = self.env["kw.participante"]
        Inscripcion = self.env["kw.inscripcion"]

        # Crear participante e inscripción confirmada
        participante = Participante.create({"name": "Ana Test"})
        Inscripcion.create({
            "taller_id": taller.id,
            "participante_id": participante.id,
            "estado": "confirmado",
        })
        taller.invalidate_recordset()
        self.assertEqual(taller.plazas_disponibles, 4)

    def test_plazas_no_bajan_con_interesados(self):
        taller = self.Taller.create(self._taller_base(max_cupos=5))
        Participante = self.env["kw.participante"]
        Inscripcion = self.env["kw.inscripcion"]

        participante = Participante.create({"name": "Pedro Test"})
        Inscripcion.create({
            "taller_id": taller.id,
            "participante_id": participante.id,
            "estado": "interesado",    # no confirmado
        })
        taller.invalidate_recordset()
        self.assertEqual(taller.plazas_disponibles, 5)

    def test_plazas_vuelven_a_subir_al_cancelar_inscripcion(self):
        taller = self.Taller.create(self._taller_base(max_cupos=3))
        Participante = self.env["kw.participante"]
        Inscripcion = self.env["kw.inscripcion"]

        participante = Participante.create({"name": "Luis Test"})
        inscripcion = Inscripcion.create({
            "taller_id": taller.id,
            "participante_id": participante.id,
            "estado": "confirmado",
        })
        taller.invalidate_recordset()
        self.assertEqual(taller.plazas_disponibles, 2)

        inscripcion.action_cancelar()
        taller.invalidate_recordset()
        self.assertEqual(taller.plazas_disponibles, 3)

    # ------------------------------------------------------------------
    # Campos requeridos y selección
    # ------------------------------------------------------------------

    def test_err_crear_sin_nombre(self):
        with self.assertRaises(Exception):
            self.Taller.create(self._taller_base(name=False))

    def test_err_crear_sin_coding_level(self):
        with self.assertRaises(Exception):
            self.Taller.create(self._taller_base(coding_level=False))

    def test_niveles_disponibles(self):
        for nivel in ("wawa", "mashi", "yachak"):
            taller = self.Taller.create(self._taller_base(
                name=f"Taller {nivel}", coding_level=nivel
            ))
            self.assertEqual(taller.coding_level, nivel)

    def test_modalidades_disponibles(self):
        for modalidad in ("virtual", "presencial", "hibrido"):
            taller = self.Taller.create(self._taller_base(
                name=f"Taller {modalidad}", modalidad=modalidad
            ))
            self.assertEqual(taller.modalidad, modalidad)
