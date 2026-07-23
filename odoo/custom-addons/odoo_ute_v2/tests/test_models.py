from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("odoo_ute_v2", "post_install", "-at_install")


class TestOdooUteV2(TransactionCase):

    def test_01_materia_valida(self):
        materia = self.env["ou.signature"].create(
            {
                "name": "Programación II",
            }
        )

        self.assertTrue(materia.id)
        self.assertEqual(
            materia.name,
            "Programación II",
        )

    def test_02_materia_solo_numeros_es_invalida(self):
        with self.assertRaises(ValidationError):
            self.env["ou.signature"].create(
                {
                    "name": "1234567890",
                }
            )

    def test_03_docente_valido(self):
        docente = self.env["sistema.usuarios"].create(
            {
                "name": "Ana",
                "last_name": "Pérez",
                "email": "ana.prueba@ute.edu.ec",
                "phone": "0999999999",
                # Número sintético con estructura matemática válida.
                "vat": "1712345675",
            }
        )

        self.assertTrue(docente.id)
        self.assertEqual(
            docente.vat,
            "1712345675",
        )

    def test_04_docente_nombre_con_numeros_es_invalido(self):
        with self.assertRaises(ValidationError):
            self.env["sistema.usuarios"].create(
                {
                    "name": "Ana123",
                    "last_name": "Pérez",
                    "email": "nombre.invalido@ute.edu.ec",
                    "phone": "0999999999",
                    "vat": "1712345675",
                }
            )

    def test_05_docente_telefono_corto_es_invalido(self):
        with self.assertRaises(ValidationError):
            self.env["sistema.usuarios"].create(
                {
                    "name": "Ana",
                    "last_name": "Pérez",
                    "email": "telefono.invalido@ute.edu.ec",
                    "phone": "123",
                    "vat": "1712345675",
                }
            )

    def test_06_cedula_con_menos_de_10_digitos_es_invalida(self):
        with self.assertRaises(ValidationError):
            self.env["sistema.usuarios"].create(
                {
                    "name": "Ana",
                    "last_name": "Pérez",
                    "email": "cedula.corta@ute.edu.ec",
                    "phone": "0999999999",
                    "vat": "1712345",
                }
            )

    def test_07_cedula_con_letras_es_invalida(self):
        with self.assertRaises(ValidationError):
            self.env["sistema.usuarios"].create(
                {
                    "name": "Ana",
                    "last_name": "Pérez",
                    "email": "cedula.letras@ute.edu.ec",
                    "phone": "0999999999",
                    "vat": "17123456AB",
                }
            )

    def test_08_cedula_con_verificador_incorrecto_es_invalida(self):
        with self.assertRaises(ValidationError):
            self.env["sistema.usuarios"].create(
                {
                    "name": "Ana",
                    "last_name": "Pérez",
                    "email": "cedula.verificador@ute.edu.ec",
                    "phone": "0999999999",
                    "vat": "1712345678",
                }
            )

    def test_09_carrera_valida(self):
        carrera = self.env["ou.carrera"].create(
            {
                "name": "Desarrollo de Software",
                "codigo": "TDS",
                "modalidad": "presencial",
            }
        )

        self.assertTrue(carrera.id)

    def test_10_carrera_solo_numeros_es_invalida(self):
        with self.assertRaises(ValidationError):
            self.env["ou.carrera"].create(
                {
                    "name": "1234567890",
                    "codigo": "TDS2",
                    "modalidad": "presencial",
                }
            )

    def test_11_periodo_valido(self):
        periodo = self.env["ou.periodo"].create(
            {
                "name": "2025-2",
                "fecha_inicio": "2025-10-01",
                "fecha_fin": "2026-02-28",
                "activo": True,
            }
        )

        self.assertTrue(periodo.id)

    def test_12_periodo_fechas_invertidas_es_invalido(self):
        with self.assertRaises(ValidationError):
            self.env["ou.periodo"].create(
                {
                    "name": "2025-2",
                    "fecha_inicio": "2026-02-01",
                    "fecha_fin": "2025-10-01",
                    "activo": True,
                }
            )

    def test_13_aula_valida(self):
        aula = self.env["ou.aula"].create(
            {
                "name": "Aula 301",
                "edificio": "Bloque A",
                "capacidad": 30,
            }
        )

        self.assertTrue(aula.id)

    def test_14_aula_capacidad_cero_es_invalida(self):
        with self.assertRaises(ValidationError):
            self.env["ou.aula"].create(
                {
                    "name": "Aula 302",
                    "edificio": "Bloque A",
                    "capacidad": 0,
                }
            )

    def test_15_aula_solo_numeros_es_invalida(self):
        with self.assertRaises(ValidationError):
            self.env["ou.aula"].create(
                {
                    "name": "301",
                    "edificio": "Bloque A",
                    "capacidad": 30,
                }
            )