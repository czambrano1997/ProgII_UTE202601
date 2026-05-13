"""
tests/test_inscripcion.py
=========================
Tests de integración para kw.inscripcion.

Cubre el flujo completo de inscripción: validaciones de cupo, taller activo,
duplicados, transiciones de estado y acciones de botón.

Ejecutar con:
    odoo-bin -d <db> --test-enable -i kodigowasi --stop-after-init
"""

from datetime import date, timedelta

from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("kodigowasi", "inscripcion", "-at_install", "post_install")
class TestKWInscripcionConstraints(TransactionCase):
    """Validaciones del modelo kw.inscripcion via constraint Railway."""

    # ------------------------------------------------------------------
    # Fixtures
    # ------------------------------------------------------------------

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Taller = cls.env["kw.taller"]
        cls.Participante = cls.env["kw.participante"]
        cls.Inscripcion = cls.env["kw.inscripcion"]

    def _taller_futuro(self, max_cupos=10, **kwargs) -> object:
        """Taller válido con fecha inicio mañana."""
        manana = date.today() + timedelta(days=1)
        vals = {
            "name": "Taller Integración",
            "coding_level": "wawa",
            "max_cupos": max_cupos,
            "fecha_inicio": manana,
            "fecha_fin": manana + timedelta(days=30),
            "modalidad": "virtual",
        }
        vals.update(kwargs)
        return self.Taller.create(vals)

    def _taller_pasado(self, **kwargs) -> object:
        """Taller cuya fecha inicio ya pasó."""
        ayer = date.today() - timedelta(days=1)
        vals = {
            "name": "Taller Pasado",
            "coding_level": "mashi",
            "max_cupos": 10,
            "fecha_inicio": ayer,
            "fecha_fin": ayer + timedelta(days=30),
            "modalidad": "presencial",
        }
        vals.update(kwargs)
        return self.Taller.create(vals)

    def _participante(self, nombre="Participante Test") -> object:
        return self.Participante.create({"name": nombre})

    def _inscripcion(self, taller, participante, estado="interesado") -> object:
        return self.Inscripcion.create({
            "taller_id": taller.id,
            "participante_id": participante.id,
            "estado": estado,
        })

    # ------------------------------------------------------------------
    # Caminos Ok: inscripción válida
    # ------------------------------------------------------------------

    def test_ok_crear_inscripcion_interesado(self):
        taller = self._taller_futuro()
        participante = self._participante()
        inscripcion = self._inscripcion(taller, participante, "interesado")
        self.assertEqual(inscripcion.estado, "interesado")

    def test_ok_crear_inscripcion_confirmada_con_cupo(self):
        taller = self._taller_futuro(max_cupos=5)
        participante = self._participante()
        inscripcion = self._inscripcion(taller, participante, "confirmado")
        self.assertEqual(inscripcion.estado, "confirmado")

    def test_ok_multiples_participantes_distintos_mismo_taller(self):
        taller = self._taller_futuro(max_cupos=3)
        for i in range(3):
            p = self._participante(f"Participante {i}")
            self._inscripcion(taller, p, "confirmado")
        taller.invalidate_recordset()
        self.assertEqual(taller.plazas_disponibles, 0)

    def test_ok_mismo_participante_en_talleres_distintos(self):
        t1 = self._taller_futuro(name="Taller A")
        t2 = self._taller_futuro(name="Taller B")
        participante = self._participante()
        self._inscripcion(t1, participante, "confirmado")
        self._inscripcion(t2, participante, "confirmado")   # no debe fallar

    def test_ok_taller_sin_fechas_permite_confirmar(self):
        taller = self.Taller.create({
            "name": "Taller Sin Fechas",
            "coding_level": "wawa",
            "max_cupos": 10,
            "modalidad": "virtual",
        })
        participante = self._participante()
        inscripcion = self._inscripcion(taller, participante, "confirmado")
        self.assertEqual(inscripcion.estado, "confirmado")

    # ------------------------------------------------------------------
    # Caminos Err: taller lleno
    # ------------------------------------------------------------------

    def test_err_taller_sin_cupo(self):
        taller = self._taller_futuro(max_cupos=1)
        p1 = self._participante("Primero")
        p2 = self._participante("Segundo")
        self._inscripcion(taller, p1, "confirmado")
        with self.assertRaises(ValidationError):
            self._inscripcion(taller, p2, "confirmado")

    def test_err_taller_cupo_maximo_cero(self):
        taller = self._taller_futuro(max_cupos=0)
        participante = self._participante()
        with self.assertRaises(ValidationError):
            self._inscripcion(taller, participante, "confirmado")

    # ------------------------------------------------------------------
    # Caminos Err: taller ya comenzó
    # ------------------------------------------------------------------

    def test_err_taller_ya_comenzo(self):
        taller = self._taller_pasado()
        participante = self._participante()
        with self.assertRaises(ValidationError):
            self._inscripcion(taller, participante, "confirmado")

    def test_ok_interesado_en_taller_pasado_no_valida(self):
        """Estado interesado no dispara el constraint."""
        taller = self._taller_pasado()
        participante = self._participante()
        inscripcion = self._inscripcion(taller, participante, "interesado")
        self.assertEqual(inscripcion.estado, "interesado")

    # ------------------------------------------------------------------
    # Caminos Err: participante duplicado
    # ------------------------------------------------------------------

    def test_err_participante_ya_confirmado_en_mismo_taller(self):
        taller = self._taller_futuro()
        participante = self._participante()
        self._inscripcion(taller, participante, "confirmado")
        with self.assertRaises(ValidationError):
            # Segunda inscripción confirmada del mismo participante en el mismo taller
            self._inscripcion(taller, participante, "confirmado")

    def test_ok_participante_cancelado_puede_reinscribirse_como_interesado(self):
        """Un participante cancelado puede volver a estar interesado."""
        taller = self._taller_futuro()
        participante = self._participante()
        primera = self._inscripcion(taller, participante, "confirmado")
        primera.action_cancelar()
        # Nueva inscripción como interesado no viola constraint
        nueva = self._inscripcion(taller, participante, "interesado")
        self.assertEqual(nueva.estado, "interesado")

    # ------------------------------------------------------------------
    # Transiciones de estado: action_confirmar / action_cancelar
    # ------------------------------------------------------------------

    def test_action_confirmar_cambia_estado_a_confirmado(self):
        taller = self._taller_futuro()
        participante = self._participante()
        inscripcion = self._inscripcion(taller, participante, "interesado")
        inscripcion.action_confirmar()
        self.assertEqual(inscripcion.estado, "confirmado")

    def test_action_cancelar_cambia_estado_a_cancelado(self):
        taller = self._taller_futuro()
        participante = self._participante()
        inscripcion = self._inscripcion(taller, participante, "interesado")
        inscripcion.action_cancelar()
        self.assertEqual(inscripcion.estado, "cancelado")

    def test_action_cancelar_libera_plaza(self):
        taller = self._taller_futuro(max_cupos=2)
        p1 = self._participante("P1")
        p2 = self._participante("P2")
        i1 = self._inscripcion(taller, p1, "confirmado")
        self._inscripcion(taller, p2, "confirmado")
        taller.invalidate_recordset()
        self.assertEqual(taller.plazas_disponibles, 0)

        i1.action_cancelar()
        taller.invalidate_recordset()
        self.assertEqual(taller.plazas_disponibles, 1)

    def test_confirmar_cuando_taller_lleno_lanza_error(self):
        """
        Cambiar estado de interesado → confirmado debe fallar si no hay cupo.
        """
        taller = self._taller_futuro(max_cupos=1)
        p1 = self._participante("P1 primero")
        p2 = self._participante("P2 segundo")
        self._inscripcion(taller, p1, "confirmado")
        inscripcion_p2 = self._inscripcion(taller, p2, "interesado")
        with self.assertRaises(ValidationError):
            inscripcion_p2.action_confirmar()


@tagged("kodigowasi", "inscripcion", "-at_install", "post_install")
class TestKWInscripcionFlujoCompleto(TransactionCase):
    """
    Prueba el flujo end-to-end de inscripción simulando el ciclo de vida
    completo: creación → confirmación → pago → completado.
    """

    def setUp(self):
        super().setUp()
        manana = date.today() + timedelta(days=1)
        self.taller = self.env["kw.taller"].create({
            "name": "Python desde Cero",
            "coding_level": "wawa",
            "max_cupos": 5,
            "fecha_inicio": manana,
            "fecha_fin": manana + timedelta(days=30),
            "modalidad": "virtual",
            "precio": 50.0,
        })
        self.participante = self.env["kw.participante"].create({
            "name": "María Kuri",
            "email": "maria@test.com",
            "nivel_actual": "wawa",
        })

    def test_flujo_interesado_a_confirmado(self):
        inscripcion = self.env["kw.inscripcion"].create({
            "taller_id": self.taller.id,
            "participante_id": self.participante.id,
            "estado": "interesado",
        })
        self.assertEqual(inscripcion.estado, "interesado")
        inscripcion.action_confirmar()
        self.assertEqual(inscripcion.estado, "confirmado")

    def test_flujo_confirmado_con_pago(self):
        inscripcion = self.env["kw.inscripcion"].create({
            "taller_id": self.taller.id,
            "participante_id": self.participante.id,
            "estado": "confirmado",
        })
        pago = self.env["kw.pago"].create({
            "inscripcion_id": inscripcion.id,
            "monto": 50.0,
            "metodo": "transferencia",
            "referencia": "REF-001",
        })
        inscripcion.write({"pago_realizado": True})
        self.assertTrue(inscripcion.pago_realizado)
        self.assertEqual(len(inscripcion.pago_ids), 1)
        self.assertEqual(pago.monto, 50.0)

    def test_flujo_cancelar_y_reabrir_como_interesado(self):
        inscripcion = self.env["kw.inscripcion"].create({
            "taller_id": self.taller.id,
            "participante_id": self.participante.id,
            "estado": "confirmado",
        })
        inscripcion.action_cancelar()
        self.assertEqual(inscripcion.estado, "cancelado")

        # Crear nueva inscripción como interesado
        nueva = self.env["kw.inscripcion"].create({
            "taller_id": self.taller.id,
            "participante_id": self.participante.id,
            "estado": "interesado",
        })
        self.assertEqual(nueva.estado, "interesado")

    def test_taller_llena_capacidad_progresivamente(self):
        Participante = self.env["kw.participante"]
        Inscripcion = self.env["kw.inscripcion"]

        for i in range(5):
            p = Participante.create({"name": f"Participante {i+1}"})
            Inscripcion.create({
                "taller_id": self.taller.id,
                "participante_id": p.id,
                "estado": "confirmado",
            })

        self.taller.invalidate_recordset()
        self.assertEqual(self.taller.plazas_disponibles, 0)

        # El participante 6 no puede confirmar
        p6 = Participante.create({"name": "Participante 6"})
        with self.assertRaises(ValidationError):
            Inscripcion.create({
                "taller_id": self.taller.id,
                "participante_id": p6.id,
                "estado": "confirmado",
            })
