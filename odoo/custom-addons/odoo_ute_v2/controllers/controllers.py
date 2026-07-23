import logging

from psycopg2 import IntegrityError

from odoo import http
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.http import request


_logger = logging.getLogger(__name__)


MODEL_CONFIG = {
    "signature": {
        "model": "ou.signature",
        "fields": ["name"],
        "required": ["name"],
        "label": "materia",
    },
    "usuarios": {
        "model": "sistema.usuarios",
        "fields": [
            "name",
            "last_name",
            "email",
            "phone",
            "vat",
        ],
        "required": [
            "name",
            "last_name",
            "email",
            "phone",
            "vat",
        ],
        "label": "docente",
    },
    "carrera": {
        "model": "ou.carrera",
        "fields": [
            "name",
            "codigo",
            "modalidad",
        ],
        "required": [
            "name",
            "codigo",
            "modalidad",
        ],
        "label": "carrera",
    },
    "periodo": {
        "model": "ou.periodo",
        "fields": [
            "name",
            "fecha_inicio",
            "fecha_fin",
            "activo",
        ],
        "required": [
            "name",
            "fecha_inicio",
            "fecha_fin",
        ],
        "label": "periodo",
    },
    "aula": {
        "model": "ou.aula",
        "fields": [
            "name",
            "edificio",
            "capacidad",
        ],
        "required": [
            "name",
            "edificio",
            "capacidad",
        ],
        "label": "aula",
    },
}


class ApiUteController(http.Controller):

    @staticmethod
    def _respuesta(
        status,
        message,
        data=None,
        http_status=200,
    ):
        contenido = {
            "status": status,
            "message": message,
        }

        if data is not None:
            contenido["data"] = data

        return request.make_json_response(
            contenido,
            status=http_status,
        )

    @staticmethod
    def _config(modelo):
        return MODEL_CONFIG[modelo]

    def _leer_json(self):
        try:
            datos = request.httprequest.get_json(
                silent=False
            )
        except Exception:
            return None, self._respuesta(
                "error",
                "El cuerpo de la petición debe contener JSON válido.",
                http_status=400,
            )

        if not isinstance(datos, dict):
            return None, self._respuesta(
                "error",
                "El contenido JSON debe ser un objeto.",
                http_status=400,
            )

        return datos, None

    @staticmethod
    def _limpiar_valores(datos, campos):
        valores = {}

        for campo in campos:
            if campo not in datos:
                continue

            valor = datos[campo]

            if isinstance(valor, str):
                valor = valor.strip()

            valores[campo] = valor

        if isinstance(valores.get("codigo"), str):
            valores["codigo"] = (
                valores["codigo"].upper()
            )

        if isinstance(valores.get("email"), str):
            valores["email"] = (
                valores["email"].lower()
            )

        return valores

    def _validar_tipos(self, modelo, valores):
        if modelo == "carrera":
            modalidades = {
                "presencial",
                "virtual",
                "hibrida",
            }

            if valores.get("modalidad") not in modalidades:
                return self._respuesta(
                    "error",
                    "La modalidad debe ser presencial, "
                    "virtual o hibrida.",
                    http_status=400,
                )

        if modelo == "aula":
            capacidad = valores.get("capacidad")

            if (
                isinstance(capacidad, bool)
                or not isinstance(capacidad, int)
            ):
                return self._respuesta(
                    "error",
                    "La capacidad debe ser un número entero.",
                    http_status=400,
                )

        if modelo == "periodo" and "activo" in valores:
            if not isinstance(valores["activo"], bool):
                return self._respuesta(
                    "error",
                    "El campo activo debe ser verdadero o falso.",
                    http_status=400,
                )

        return None

    def _listar(self, modelo):
        config = self._config(modelo)

        try:
            campos = [
                "id",
                *config["fields"],
            ]

            registros = (
                request.env[config["model"]]
                .sudo()
                .search([])
                .read(campos)
            )

            return self._respuesta(
                "success",
                (
                    f"{len(registros)} registro(s) de "
                    f"{config['label']} obtenido(s) correctamente."
                ),
                registros,
            )

        except Exception:
            _logger.exception(
                "Error al listar el modelo %s",
                modelo,
            )
            request.env.cr.rollback()

            return self._respuesta(
                "error",
                "No se pudieron obtener los registros.",
                http_status=500,
            )

    def _crear(self, modelo):
        config = self._config(modelo)

        datos, error = self._leer_json()

        if error:
            return error

        valores = self._limpiar_valores(
            datos,
            config["fields"],
        )

        faltantes = []

        for campo in config["required"]:
            if (
                campo not in valores
                or valores[campo] is None
                or valores[campo] == ""
            ):
                faltantes.append(campo)

        if faltantes:
            return self._respuesta(
                "error",
                (
                    "Faltan campos obligatorios: "
                    + ", ".join(faltantes)
                ),
                http_status=400,
            )

        error_tipo = self._validar_tipos(
            modelo,
            valores,
        )

        if error_tipo:
            return error_tipo

        try:
            registro = (
                request.env[config["model"]]
                .sudo()
                .create(valores)
            )

            return self._respuesta(
                "success",
                (
                    f"{config['label'].capitalize()} "
                    "creado correctamente."
                ),
                {
                    "id": registro.id,
                },
            )

        except (
            ValidationError,
            UserError,
            AccessError,
            ValueError,
            TypeError,
        ) as exc:
            request.env.cr.rollback()

            return self._respuesta(
                "error",
                str(exc),
                http_status=400,
            )

        except IntegrityError:
            request.env.cr.rollback()

            return self._respuesta(
                "error",
                (
                    "El registro está duplicado o incumple "
                    "una restricción."
                ),
                http_status=409,
            )

        except Exception:
            _logger.exception(
                "Error al crear el modelo %s",
                modelo,
            )
            request.env.cr.rollback()

            return self._respuesta(
                "error",
                "No se pudo crear el registro.",
                http_status=500,
            )

    def _eliminar(self, modelo, record_id):
        config = self._config(modelo)

        try:
            registro = (
                request.env[config["model"]]
                .sudo()
                .browse(record_id)
            )

            if not registro.exists():
                return self._respuesta(
                    "error",
                    "El registro solicitado no existe.",
                    http_status=404,
                )

            registro.unlink()

            return self._respuesta(
                "success",
                (
                    f"{config['label'].capitalize()} "
                    "eliminado correctamente."
                ),
                {
                    "id": record_id,
                },
            )

        except (
            ValidationError,
            UserError,
            AccessError,
        ) as exc:
            request.env.cr.rollback()

            return self._respuesta(
                "error",
                str(exc),
                http_status=400,
            )

        except IntegrityError:
            request.env.cr.rollback()

            return self._respuesta(
                "error",
                (
                    "No se puede eliminar porque el registro "
                    "está relacionado con otros datos."
                ),
                http_status=409,
            )

        except Exception:
            _logger.exception(
                "Error al eliminar %s con ID %s",
                modelo,
                record_id,
            )
            request.env.cr.rollback()

            return self._respuesta(
                "error",
                "No se pudo eliminar el registro.",
                http_status=500,
            )

    @http.route(
        "/api_ute/signature/all",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
        cors="*",
    )
    def signature_all(self, **kwargs):
        return self._listar("signature")

    @http.route(
        "/api_ute/signature/create",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False,
        cors="*",
    )
    def signature_create(self, **kwargs):
        return self._crear("signature")

    @http.route(
        "/api_ute/signature/delete/<int:record_id>",
        type="http",
        auth="public",
        methods=["DELETE"],
        csrf=False,
        cors="*",
    )
    def signature_delete(self, record_id, **kwargs):
        return self._eliminar(
            "signature",
            record_id,
        )

    @http.route(
        "/api_ute/usuarios/all",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
        cors="*",
    )
    def usuarios_all(self, **kwargs):
        return self._listar("usuarios")

    @http.route(
        "/api_ute/usuarios/create",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False,
        cors="*",
    )
    def usuarios_create(self, **kwargs):
        return self._crear("usuarios")

    @http.route(
        "/api_ute/usuarios/delete/<int:record_id>",
        type="http",
        auth="public",
        methods=["DELETE"],
        csrf=False,
        cors="*",
    )
    def usuarios_delete(self, record_id, **kwargs):
        return self._eliminar(
            "usuarios",
            record_id,
        )

    @http.route(
        "/api_ute/carrera/all",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
        cors="*",
    )
    def carrera_all(self, **kwargs):
        return self._listar("carrera")

    @http.route(
        "/api_ute/carrera/create",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False,
        cors="*",
    )
    def carrera_create(self, **kwargs):
        return self._crear("carrera")

    @http.route(
        "/api_ute/carrera/delete/<int:record_id>",
        type="http",
        auth="public",
        methods=["DELETE"],
        csrf=False,
        cors="*",
    )
    def carrera_delete(self, record_id, **kwargs):
        return self._eliminar(
            "carrera",
            record_id,
        )

    @http.route(
        "/api_ute/periodo/all",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
        cors="*",
    )
    def periodo_all(self, **kwargs):
        return self._listar("periodo")

    @http.route(
        "/api_ute/periodo/create",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False,
        cors="*",
    )
    def periodo_create(self, **kwargs):
        return self._crear("periodo")

    @http.route(
        "/api_ute/periodo/delete/<int:record_id>",
        type="http",
        auth="public",
        methods=["DELETE"],
        csrf=False,
        cors="*",
    )
    def periodo_delete(self, record_id, **kwargs):
        return self._eliminar(
            "periodo",
            record_id,
        )

    @http.route(
        "/api_ute/aula/all",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
        cors="*",
    )
    def aula_all(self, **kwargs):
        return self._listar("aula")

    @http.route(
        "/api_ute/aula/create",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False,
        cors="*",
    )
    def aula_create(self, **kwargs):
        return self._crear("aula")

    @http.route(
        "/api_ute/aula/delete/<int:record_id>",
        type="http",
        auth="public",
        methods=["DELETE"],
        csrf=False,
        cors="*",
    )
    def aula_delete(self, record_id, **kwargs):
        return self._eliminar(
            "aula",
            record_id,
        )
