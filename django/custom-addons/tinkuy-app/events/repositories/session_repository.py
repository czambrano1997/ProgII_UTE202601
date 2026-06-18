from __future__ import annotations

from django.db.models import QuerySet, Prefetch

from events.models import Session, Speaker


def list_by_event(event_id: int) -> QuerySet[Session]:
    return (
        Session.objects.filter(event_id=event_id)
        .select_related("room")
        .prefetch_related(
            Prefetch("speakers", queryset=Speaker.objects.all())
        )
        .order_by("scheduled_at")
    )


def get_by_slug(event_id: int, slug: str) -> Session | None:
    return Session.objects.filter(event_id=event_id, slug=slug).first()


def list_keynotes(event_id: int) -> QuerySet[Session]:
    return Session.objects.filter(event_id=event_id, is_keynote=True).order_by("scheduled_at")


def list_by_room(room_id: int) -> QuerySet[Session]:
    return Session.objects.filter(room_id=room_id).select_related("event").order_by("scheduled_at")
