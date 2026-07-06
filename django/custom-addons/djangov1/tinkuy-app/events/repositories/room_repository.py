from __future__ import annotations

from django.db.models import QuerySet

from events.models import Room

# ---------------------------------------------------------------------------
# Reads
# ---------------------------------------------------------------------------


def list_all() -> QuerySet[Room]:
    return Room.objects.all()


def get_by_id(pk: int) -> Room | None:
    return Room.objects.filter(pk=pk).first()


def get_by_name(name: str) -> Room | None:
    return Room.objects.filter(name=name).first()


# ---------------------------------------------------------------------------
# Writes — the only ORM write path for Room (ADR-0001, ADR-0006)
# ---------------------------------------------------------------------------


def create(
    *,
    name: str,
    floor: int,
    seating_capacity: int,
    has_projector: bool = True,
    notes: str = "",
) -> Room:
    return Room.objects.create(
        name=name,
        floor=floor,
        seating_capacity=seating_capacity,
        has_projector=has_projector,
        notes=notes,
    )


def update(
    room_id: int,
    *,
    name: str | None = None,
    floor: int | None = None,
    seating_capacity: int | None = None,
    has_projector: bool | None = None,
    notes: str | None = None,
) -> Room | None:
    """Partial update: only the fields passed (non-``None``) are written."""
    room = Room.objects.filter(pk=room_id).first()
    if room is None:
        return None
    if name is not None:
        room.name = name
    if floor is not None:
        room.floor = floor
    if seating_capacity is not None:
        room.seating_capacity = seating_capacity
    if has_projector is not None:
        room.has_projector = has_projector
    if notes is not None:
        room.notes = notes
    room.save()
    return room


def delete(room_id: int) -> bool:
    deleted, _ = Room.objects.filter(pk=room_id).delete()
    return deleted > 0


def get_or_create(
    *,
    name: str,
    floor: int,
    seating_capacity: int,
    has_projector: bool = True,
    notes: str = "",
) -> tuple[Room, bool]:
    """Idempotent create keyed on the natural key ``name`` (seeding path)."""
    return Room.objects.get_or_create(
        name=name,
        defaults={
            "floor": floor,
            "seating_capacity": seating_capacity,
            "has_projector": has_projector,
            "notes": notes,
        },
    )
