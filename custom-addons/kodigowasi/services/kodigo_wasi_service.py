from ..shared.result import Ok, Err, Result, combine, from_exception
from datetime import date, datetime


class KodigoWasiService:
    """Servicio con lógica de negocio para KodigoWasi."""

    @staticmethod
    def check_taller_fechas(
        fecha_inicio: date, fecha_fin: date
    ) -> Result[None, str]:
        if fecha_inicio and fecha_fin and fecha_fin <= fecha_inicio:
            return Err("La fecha de fin debe ser posterior a la de inicio.")
        return Ok(None)

    @staticmethod
    def check_cupo_disponible(
        max_cupos: int, plazas_ocupadas: int, nombre_taller: str
    ) -> Result[None, str]:
        if max_cupos <= 0:
            return Err(f"El taller '{nombre_taller}' debe tener un cupo positivo.")
        if plazas_ocupadas >= max_cupos:
            return Err(f"No hay cupo en el taller '{nombre_taller}'.")
        return Ok(None)

    @staticmethod
    def check_taller_activo(inicio: date, nombre: str) -> Result[None, str]:
        if inicio and date.today() > inicio:
            return Err(f"El taller '{nombre}' ya comenzó. No se permiten nuevas inscripciones.")
        return Ok(None)

    @staticmethod
    def validar_inscripcion(taller, participante) -> Result[None, str]:
        # Obtener plazas ocupadas confirmadas
        plazas_confirmadas = taller.inscripcion_ids.filtered(
            lambda i: i.estado == 'confirmado'
        )
        # Encadenar validaciones con combine (Railway)
        validaciones = combine([
            KodigoWasiService.check_taller_fechas(
                taller.fecha_inicio, taller.fecha_fin
            ).alt(lambda e: e),  # alt no cambia nada porque ya es Err/Ok
            KodigoWasiService.check_cupo_disponible(
                taller.max_cupos, len(plazas_confirmadas), taller.name
            ),
            KodigoWasiService.check_taller_activo(taller.fecha_inicio, taller.name),
        ])

        # Si ya está inscrito y confirmado? Podríamos añadir otra validación.
        if participante.inscripcion_ids.filtered(
            lambda i: i.taller_id == taller and i.estado == 'confirmado'
        ):
            return Err("El participante ya está confirmado en este taller.")

        return validaciones

    @staticmethod
    def calcular_precio_por_nivel(nivel: str) -> float:
        """Ejemplo de lógica de negocio para onchange."""
        precios = {
            'wawa': 50.0,
            'mashi': 100.0,
            'yachak': 200.0,
        }
        return precios.get(nivel, 0.0)