from __future__ import annotations

from datetime import datetime, time, timedelta
from typing import Sequence

from django.db import transaction
from django.db.models import Prefetch, QuerySet

from events.models import Session, Speaker

# ---------------------------------------------------------------------------
# Reads
# ---------------------------------------------------------------------------


def list_by_event(event_id: int) -> QuerySet[Session]:
    return (
        Session.objects.filter(event_id=event_id)
        .select_related("room")
        .prefetch_related(
            Prefetch("speakers", queryset=Speaker.objects.all())
        )
        .order_by("scheduled_at")
    )


def list_all() -> QuerySet[Session]:
    return (
        Session.objects.select_related("event", "room")
        .prefetch_related("speakers")
        .all()
    )


def get_by_id(pk: int) -> Session | None:
    return Session.objects.filter(pk=pk).first()


def get_by_slug(event_id: int, slug: str) -> Session | None:
    return Session.objects.filter(event_id=event_id, slug=slug).first()


def list_keynotes(event_id: int) -> QuerySet[Session]:
    return Session.objects.filter(event_id=event_id, is_keynote=True).order_by("scheduled_at")


def list_by_room(room_id: int) -> QuerySet[Session]:
    return Session.objects.filter(room_id=room_id).select_related("event").order_by("scheduled_at")


# ---------------------------------------------------------------------------
# Writes — the only ORM write path for Session.
# The ``speakers`` M2M is attached in the same transaction; the
# ``unique_together(event, slug)`` constraint is the natural key (ADR-0006).
# ---------------------------------------------------------------------------


def create(
    *,
    event_id: int,
    room_id: int,
    title: str,
    slug: str,
    abstract: str,
    level: str,
    scheduled_at: datetime,
    start_time: time,
    duration: timedelta,
    max_seats: int,
    speaker_ids: Sequence[int] = (),
    is_keynote: bool = False,
    recording_url: str = "",
) -> Session:
    with transaction.atomic():
        session = Session.objects.create(
            event_id=event_id,
            room_id=room_id,
            title=title,
            slug=slug,
            abstract=abstract,
            level=level,
            scheduled_at=scheduled_at,
            start_time=start_time,
            duration=duration,
            max_seats=max_seats,
            is_keynote=is_keynote,
            recording_url=recording_url,
        )
        if speaker_ids:
            session.speakers.set(Speaker.objects.filter(pk__in=speaker_ids))
        return session


def update(
    session_id: int,
    *,
    room_id: int | None = None,
    title: str | None = None,
    slug: str | None = None,
    abstract: str | None = None,
    level: str | None = None,
    scheduled_at: datetime | None = None,
    start_time: time | None = None,
    duration: timedelta | None = None,
    max_seats: int | None = None,
    is_keynote: bool | None = None,
    recording_url: str | None = None,
    speaker_ids: Sequence[int] | None = None,
) -> Session | None:
    """Partial update. ``speaker_ids`` (when given) replaces the M2M set."""
    with transaction.atomic():
        session = Session.objects.filter(pk=session_id).first()
        if session is None:
            return None
        if room_id is not None:
            session.room_id = room_id
        if title is not None:
            session.title = title
        if slug is not None:
            session.slug = slug
        if abstract is not None:
            session.abstract = abstract
        if level is not None:
            session.level = level
        if scheduled_at is not None:
            session.scheduled_at = scheduled_at
        if start_time is not None:
            session.start_time = start_time
        if duration is not None:
            session.duration = duration
        if max_seats is not None:
            session.max_seats = max_seats
        if is_keynote is not None:
            session.is_keynote = is_keynote
        if recording_url is not None:
            session.recording_url = recording_url
        session.save()
        if speaker_ids is not None:
            session.speakers.set(Speaker.objects.filter(pk__in=speaker_ids))
        return session


def delete(session_id: int) -> bool:
    deleted, _ = Session.objects.filter(pk=session_id).delete()
    return deleted > 0


def get_or_create(
    *,
    event_id: int,
    slug: str,
    room_id: int,
    title: str,
    abstract: str,
    level: str,
    scheduled_at: datetime,
    start_time: time,
    duration: timedelta,
    max_seats: int,
    speaker_ids: Sequence[int] = (),
    is_keynote: bool = False,
    recording_url: str = "",
) -> tuple[Session, bool]:
    """Idempotent create keyed on ``(event, slug)`` (seeding path)."""
    with transaction.atomic():
        session, created = Session.objects.get_or_create(
            event_id=event_id,
            slug=slug,
            defaults={
                "room_id": room_id,
                "title": title,
                "abstract": abstract,
                "level": level,
                "scheduled_at": scheduled_at,
                "start_time": start_time,
                "duration": duration,
                "max_seats": max_seats,
                "is_keynote": is_keynote,
                "recording_url": recording_url,
            },
        )
        if created and speaker_ids:
            session.speakers.set(Speaker.objects.filter(pk__in=speaker_ids))
        return session, created
