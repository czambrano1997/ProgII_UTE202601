"""
services/kodigo_wasi_service.py
================================
Lógica de negocio pura para KodigoWasi (sin dependencias de Odoo ORM).

Todos los métodos son estáticos y devuelven Result[T, str], lo que permite
componer validaciones en pipelines Railway sin try/except en los modelos.

Módulos cubiertos
-----------------
  Taller      : fechas, cupo, estado activo, precio por nivel
  Inscripcion : validación completa (cupo + fechas + duplicados)
  Pago        : validación de monto, cálculo de total, completitud de pago
  Sesion      : fechas dentro del taller, duración mínima
  Instructor  : email, disponibilidad por solapamiento de talleres
  Participante: email, cédula ecuatoriana, elegibilidad para subir de nivel
"""

from __future__ import annotations

import re
from datetime import date, datetime
from typing import Any

from ..shared.result import Err, Ok, Result, combine


# ---------------------------------------------------------------------------
# Constantes de dominio
# ---------------------------------------------------------------------------

NIVELES_ORDEN: list[str] = ["wawa", "mashi", "yachak"]

PRECIOS_NIVEL: dict[str, float] = {
    "wawa": 50.0,
    "mashi": 100.0,
    "yachak": 200.0,
}

DURACION_SESION_MINIMA_MIN: int = 30    # minutos
DURACION_SESION_MAXIMA_MIN: int = 480   # 8 horas

TALLERES_PARA_SUBIR_NIVEL: int = 2      # talleres completados para ascender
EDAD_MINIMA_PARTICIPANTE: int = 15      # años


# ---------------------------------------------------------------------------
# Servicio principal
# ---------------------------------------------------------------------------

class KodigoWasiService:
    """Servicio con lógica de negocio para KodigoWasi."""

    # ------------------------------------------------------------------ #
    # Taller                                                               #
    # ------------------------------------------------------------------ #

    @staticmethod
    def check_taller_fechas(fecha_inicio: date | None, fecha_fin: date | None) -> Result[None, str]:
        """Valida que la fecha de fin sea estrictamente posterior a la de inicio."""
        if fecha_inicio and fecha_fin and fecha_fin <= fecha_inicio:
            return Err("La fecha de fin debe ser posterior a la de inicio.")
        return Ok(None)

    @staticmethod
    def check_cupo_disponible(
        max_cupos: int,
        plazas_ocupadas: int,
        nombre_taller: str,
    ) -> Result[None, str]:
        """Valida que el taller tenga cupos positivos y plazas libres."""
        if max_cupos <= 0:
            return Err(f"El taller '{nombre_taller}' debe tener un cupo positivo.")
        if plazas_ocupadas >= max_cupos:
            return Err(f"No hay cupo en el taller '{nombre_taller}'.")
        return Ok(None)

    @staticmethod
    def check_taller_activo(inicio: date | None, nombre: str) -> Result[None, str]:
        """Valida que el taller aún no haya comenzado (inscripciones abiertas)."""
        if inicio and date.today() > inicio:
            return Err(
                f"El taller '{nombre}' ya comenzó. No se permiten nuevas inscripciones."
            )
        return Ok(None)

    @staticmethod
    def calcular_precio_por_nivel(nivel: str) -> float:
        """Devuelve el precio según el nivel del taller; 0.0 para niveles desconocidos."""
        return PRECIOS_NIVEL.get(nivel, 0.0)

    # ------------------------------------------------------------------ #
    # Inscripcion                                                          #
    # ------------------------------------------------------------------ #

    @staticmethod
    def validar_inscripcion(taller: Any, participante: Any) -> Result[None, str]:
        """
        Validación completa de una nueva inscripción confirmada.

        Orden (cortocircuita en el primer Err):
          1. Fechas coherentes del taller.
          2. Cupo disponible.
          3. Taller no iniciado.
          4. Participante no duplicado en el mismo taller.
        """
        plazas_confirmadas = taller.inscripcion_ids.filtered(
            lambda i: i.estado == "confirmado"
        )
        validaciones = combine([
            KodigoWasiService.check_taller_fechas(taller.fecha_inicio, taller.fecha_fin),
            KodigoWasiService.check_cupo_disponible(
                taller.max_cupos, len(plazas_confirmadas), taller.name
            ),
            KodigoWasiService.check_taller_activo(taller.fecha_inicio, taller.name),
        ])
        if not validaciones:
            return validaciones
        if participante.inscripcion_ids.filtered(
            lambda i: i.taller_id == taller and i.estado == "confirmado"
        ):
            return Err("El participante ya está confirmado en este taller.")
        return Ok(None)

    # ------------------------------------------------------------------ #
    # Pago                                                                 #
    # ------------------------------------------------------------------ #

    @staticmethod
    def check_pago_monto_positivo(monto: float) -> Result[None, str]:
        """Valida que el monto sea estrictamente mayor que cero."""
        if monto <= 0:
            return Err("El monto del pago debe ser mayor que cero.")
        return Ok(None)

    @staticmethod
    def check_pago_no_excede_precio(
        monto_nuevo: float,
        total_pagado_previo: float,
        precio_taller: float,
    ) -> Result[None, str]:
        """
        Evita registrar un pago que supere el precio del taller.

        Si el taller es gratuito (precio <= 0) no aplica la restricción.
        """
        if precio_taller <= 0:
            return Ok(None)
        if total_pagado_previo + monto_nuevo > precio_taller:
            exceso = total_pagado_previo + monto_nuevo - precio_taller
            return Err(
                f"El pago excede el precio del taller en ${exceso:.2f}. "
                f"Precio: ${precio_taller:.2f}, ya pagado: ${total_pagado_previo:.2f}."
            )
        return Ok(None)

    @staticmethod
    def calcular_total_pagado(pagos: Any) -> float:
        """
        Suma los montos de todos los pagos de una inscripción.

        Compatible con recordsets Odoo y listas de objetos con atributo ``monto``.
        """
        return sum(p.monto for p in pagos if hasattr(p, "monto"))

    @staticmethod
    def check_pago_completo(total_pagado: float, precio_taller: float) -> Result[None, str]:
        """
        Verifica que el total pagado cubra el precio del taller.

        Talleres gratuitos (precio == 0) siempre se consideran pagados.
        """
        if precio_taller <= 0:
            return Ok(None)
        if total_pagado < precio_taller:
            pendiente = precio_taller - total_pagado
            return Err(
                f"Pago incompleto. Falta abonar ${pendiente:.2f} "
                f"(pagado: ${total_pagado:.2f} / total: ${precio_taller:.2f})."
            )
        return Ok(None)

    @staticmethod
    def validar_pago(inscripcion: Any, monto: float) -> Result[None, str]:
        """
        Validación completa de un nuevo pago sobre una inscripción.

        Valida:
          1. Monto positivo.
          2. La inscripción no está cancelada.
          3. El nuevo pago no excede el precio del taller.
        """
        resultado_monto = KodigoWasiService.check_pago_monto_positivo(monto)
        if not resultado_monto:
            return resultado_monto

        estado = getattr(inscripcion, "estado", None)
        if estado == "cancelado":
            return Err("No se puede registrar un pago en una inscripción cancelada.")

        precio_taller = getattr(inscripcion.taller_id, "precio", 0.0) or 0.0
        if precio_taller > 0:
            pagos_existentes = getattr(inscripcion, "pago_ids", [])
            total_previo = KodigoWasiService.calcular_total_pagado(pagos_existentes)
            return KodigoWasiService.check_pago_no_excede_precio(
                monto, total_previo, precio_taller
            )

        return Ok(None)

    # ------------------------------------------------------------------ #
    # Sesion                                                               #
    # ------------------------------------------------------------------ #

    @staticmethod
    def check_sesion_duracion(duracion_minutos: int) -> Result[None, str]:
        """Valida que la duración esté en el rango [30, 480] minutos."""
        if duracion_minutos < DURACION_SESION_MINIMA_MIN:
            return Err(
                f"La duración mínima de una sesión es {DURACION_SESION_MINIMA_MIN} minutos "
                f"(indicado: {duracion_minutos} min)."
            )
        if duracion_minutos > DURACION_SESION_MAXIMA_MIN:
            return Err(
                f"La duración máxima de una sesión es {DURACION_SESION_MAXIMA_MIN} minutos "
                f"(indicado: {duracion_minutos} min)."
            )
        return Ok(None)

    @staticmethod
    def check_sesion_en_rango_taller(
        fecha_sesion: datetime | None,
        fecha_inicio_taller: date | None,
        fecha_fin_taller: date | None,
        nombre_sesion: str = "Sesión",
    ) -> Result[None, str]:
        """
        Valida que la fecha de la sesión esté dentro del período del taller.

        Sin fechas de taller definidas no aplica restricción.
        """
        if not fecha_sesion:
            return Ok(None)
        if not fecha_inicio_taller and not fecha_fin_taller:
            return Ok(None)

        fecha_sesion_date = (
            fecha_sesion.date() if isinstance(fecha_sesion, datetime) else fecha_sesion
        )
        if fecha_inicio_taller and fecha_sesion_date < fecha_inicio_taller:
            return Err(
                f"'{nombre_sesion}' ({fecha_sesion_date}) es anterior al inicio "
                f"del taller ({fecha_inicio_taller})."
            )
        if fecha_fin_taller and fecha_sesion_date > fecha_fin_taller:
            return Err(
                f"'{nombre_sesion}' ({fecha_sesion_date}) es posterior al fin "
                f"del taller ({fecha_fin_taller})."
            )
        return Ok(None)

    @staticmethod
    def validar_sesion(sesion: Any, taller: Any) -> Result[None, str]:
        """
        Validación completa de una sesión dentro de su taller.

        Valida:
          1. Duración en rango permitido (si se especifica).
          2. Fecha/hora dentro del período del taller (si existen).
        """
        checks: list[Result[None, str]] = []

        duracion = getattr(sesion, "duracion_minutos", 0) or 0
        if duracion > 0:
            checks.append(KodigoWasiService.check_sesion_duracion(duracion))

        checks.append(
            KodigoWasiService.check_sesion_en_rango_taller(
                getattr(sesion, "fecha_hora", None),
                getattr(taller, "fecha_inicio", None),
                getattr(taller, "fecha_fin", None),
                getattr(sesion, "name", "Sesión"),
            )
        )

        return combine(checks).map(lambda _: None)

    # ------------------------------------------------------------------ #
    # Instructor                                                           #
    # ------------------------------------------------------------------ #

    @staticmethod
    def check_instructor_email(email: str | None) -> Result[None, str]:
        """Valida el formato del correo del instructor."""
        if not email:
            return Ok(None)
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email.strip()):
            return Err(f"El correo '{email}' no tiene un formato válido.")
        return Ok(None)

    @staticmethod
    def check_instructor_disponible(
        fecha_inicio: date | None,
        fecha_fin: date | None,
        talleres_del_instructor: Any,
        taller_id_excluir: int | None = None,
    ) -> Result[None, str]:
        """
        Verifica que el instructor no tenga otro taller en el mismo período.

        Detecta solapamiento: A.inicio <= B.fin AND A.fin >= B.inicio.
        Talleres sin fechas no se consideran conflicto.
        """
        if not fecha_inicio or not fecha_fin:
            return Ok(None)

        for taller in talleres_del_instructor:
            if taller_id_excluir and taller.id == taller_id_excluir:
                continue
            t_inicio = getattr(taller, "fecha_inicio", None)
            t_fin = getattr(taller, "fecha_fin", None)
            if not t_inicio or not t_fin:
                continue
            if fecha_inicio <= t_fin and fecha_fin >= t_inicio:
                return Err(
                    f"El instructor ya tiene asignado el taller '{taller.name}' "
                    f"({t_inicio} – {t_fin}), que se solapa con "
                    f"{fecha_inicio} – {fecha_fin}."
                )
        return Ok(None)

    # ------------------------------------------------------------------ #
    # Participante                                                         #
    # ------------------------------------------------------------------ #

    @staticmethod
    def check_participante_email(email: str | None) -> Result[None, str]:
        """Valida el formato del correo del participante."""
        if not email:
            return Ok(None)
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email.strip()):
            return Err(f"El correo '{email}' no tiene un formato válido.")
        return Ok(None)

    @staticmethod
    def check_cedula_ecuatoriana(cedula: str | None) -> Result[None, str]:
        """
        Valida la cédula ecuatoriana con el algoritmo de dígito verificador.

        Reglas:
          - 10 dígitos numéricos.
          - Primeros dos dígitos: provincia válida (01-24 ó 30).
          - Tercer dígito < 6 (persona natural).
          - Dígito verificador (posición 10) por módulo 10.
        """
        if not cedula:
            return Ok(None)
        cedula = cedula.strip().replace("-", "").replace(" ", "")
        if not cedula.isdigit() or len(cedula) != 10:
            return Err("La cédula debe tener exactamente 10 dígitos numéricos.")

        provincia = int(cedula[:2])
        if not (1 <= provincia <= 24 or provincia == 30):
            return Err(f"El código de provincia '{cedula[:2]}' no es válido.")

        if int(cedula[2]) >= 6:
            return Err("El tercer dígito de la cédula debe ser menor que 6.")

        coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
        total = 0
        for i, coef in enumerate(coeficientes):
            producto = int(cedula[i]) * coef
            total += producto - 9 if producto > 9 else producto

        digito_verificador = (10 - (total % 10)) % 10
        if digito_verificador != int(cedula[9]):
            return Err("La cédula no es válida (dígito verificador incorrecto).")
        return Ok(None)

    @staticmethod
    def check_edad_minima(
        fecha_nacimiento: date | None,
        edad_minima: int = EDAD_MINIMA_PARTICIPANTE,
    ) -> Result[None, str]:
        """Valida que el participante cumpla la edad mínima."""
        if not fecha_nacimiento:
            return Ok(None)
        hoy = date.today()
        edad = (
            hoy.year - fecha_nacimiento.year
            - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        )
        if edad < edad_minima:
            return Err(
                f"El participante debe tener al menos {edad_minima} años "
                f"(edad calculada: {edad})."
            )
        return Ok(None)

    @staticmethod
    def calcular_nivel_siguiente(nivel_actual: str) -> Result[str, str]:
        """
        Retorna el nivel inmediatamente superior al actual.

        Ok(nivel)  → existe nivel superior.
        Err(msg)   → ya está en el nivel máximo (yachak).
        """
        if nivel_actual not in NIVELES_ORDEN:
            return Err(f"Nivel desconocido: '{nivel_actual}'.")
        idx = NIVELES_ORDEN.index(nivel_actual)
        if idx >= len(NIVELES_ORDEN) - 1:
            return Err(
                f"El participante ya está en el nivel máximo ('{nivel_actual}')."
            )
        return Ok(NIVELES_ORDEN[idx + 1])

    @staticmethod
    def puede_subir_nivel(participante: Any) -> Result[str, str]:
        """
        Evalúa si el participante cumple los requisitos para ascender de nivel.

        Criterios:
          - No estar en el nivel máximo (yachak).
          - Tener al menos TALLERES_PARA_SUBIR_NIVEL talleres 'completado'
            en el nivel actual.

        Ok(nivel_siguiente)  → puede ascender.
        Err(msg)             → no cumple requisitos o ya es yachak.
        """
        nivel_actual = getattr(participante, "nivel_actual", None)
        if not nivel_actual:
            return Err("El participante no tiene un nivel asignado.")

        resultado_siguiente = KodigoWasiService.calcular_nivel_siguiente(nivel_actual)
        if not resultado_siguiente:
            return resultado_siguiente

        completados = participante.inscripcion_ids.filtered(
            lambda i: (
                i.estado == "completado"
                and getattr(i.taller_id, "coding_level", None) == nivel_actual
            )
        )
        if len(completados) < TALLERES_PARA_SUBIR_NIVEL:
            faltantes = TALLERES_PARA_SUBIR_NIVEL - len(completados)
            return Err(
                f"Se necesitan {TALLERES_PARA_SUBIR_NIVEL} talleres completados "
                f"en nivel '{nivel_actual}'. Faltan {faltantes}."
            )
        return resultado_siguiente
