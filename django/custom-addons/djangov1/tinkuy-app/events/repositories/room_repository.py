from __future__ import annotations

from django.db.models import QuerySet

from events.models import Room


def list_all() -> QuerySet[Room]:
    return Room.objects.all()


def get_by_id(pk: int) -> Room | None:
    return Room.objects.filter(pk=pk).first()
