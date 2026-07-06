from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from django.db import transaction
from django.db.models import QuerySet

from events.models import Event
from events.repositories._sql import fetchall

# ---------------------------------------------------------------------------
# Reads
# ---------------------------------------------------------------------------


def list_published() -> QuerySet[Event]:
    return Event.objects.filter(is_published=True).order_by("start_date")


def get_by_slug(slug: str) -> Event | None:
    return Event.objects.filter(slug=slug).first()


def get_by_id(pk: int) -> Event | None:
    return Event.objects.filter(pk=pk).first()


def list_all() -> QuerySet[Event]:
    return Event.objects.all()


# ---------------------------------------------------------------------------
# Writes — the only ORM write path for Event (ADR-0001, ADR-0006)
# ---------------------------------------------------------------------------


def create(
    *,
    name: str,
    slug: str,
    summary: str,
    start_date: date,
    end_date: date,
    capacity: int,
    ticket_price: Decimal,
    website: str = "",
    is_published: bool = False,
) -> Event:
    # atomic savepoint so a unique-slug violation rolls back cleanly and the
    # caller's transaction stays usable (lets the API map it to 409).
    with transaction.atomic():
        return Event.objects.create(
            name=name,
            slug=slug,
            summary=summary,
            start_date=start_date,
            end_date=end_date,
            capacity=capacity,
            ticket_price=ticket_price,
            website=website,
            is_published=is_published,
        )


def update(
    event_id: int,
    *,
    name: str | None = None,
    slug: str | None = None,
    summary: str | None = None,
    website: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    is_published: bool | None = None,
    capacity: int | None = None,
    ticket_price: Decimal | None = None,
) -> Event | None:
    """Partial update: only the fields passed (non-``None``) are written."""
    event = Event.objects.filter(pk=event_id).first()
    if event is None:
        return None
    if name is not None:
        event.name = name
    if slug is not None:
        event.slug = slug
    if summary is not None:
        event.summary = summary
    if website is not None:
        event.website = website
    if start_date is not None:
        event.start_date = start_date
    if end_date is not None:
        event.end_date = end_date
    if is_published is not None:
        event.is_published = is_published
    if capacity is not None:
        event.capacity = capacity
    if ticket_price is not None:
        event.ticket_price = ticket_price
    event.save()
    return event


def delete(event_id: int) -> bool:
    deleted, _ = Event.objects.filter(pk=event_id).delete()
    return deleted > 0


def get_or_create(
    *,
    slug: str,
    name: str,
    summary: str,
    start_date: date,
    end_date: date,
    capacity: int,
    ticket_price: Decimal,
    website: str = "",
    is_published: bool = False,
) -> tuple[Event, bool]:
    """Idempotent create keyed on the natural key ``slug`` (seeding path)."""
    return Event.objects.get_or_create(
        slug=slug,
        defaults={
            "name": name,
            "summary": summary,
            "start_date": start_date,
            "end_date": end_date,
            "capacity": capacity,
            "ticket_price": ticket_price,
            "website": website,
            "is_published": is_published,
        },
    )


# ---------------------------------------------------------------------------
# Reports (raw SQL → DTOs)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class EventAttendanceRow:
    event_id: int
    event_name: str
    total_registrations: int
    confirmed: int
    revenue: Decimal


def attendance_report() -> list[EventAttendanceRow]:
    rows = fetchall(
        """
        SELECT e.id            AS event_id,
               e.name          AS event_name,
               COUNT(r.id)     AS total_registrations,
               COUNT(r.id) FILTER (WHERE r.confirmed) AS confirmed,
               COALESCE(SUM(r.amount_paid), 0)        AS revenue
        FROM events_event e
        LEFT JOIN events_session s      ON s.event_id = e.id
        LEFT JOIN events_registration r ON r.session_id = s.id
        GROUP BY e.id, e.name
        ORDER BY revenue DESC
        """
    )
    return [
        EventAttendanceRow(
            event_id=int(row["event_id"]),
            event_name=str(row["event_name"]),
            total_registrations=int(row["total_registrations"]),
            confirmed=int(row["confirmed"]),
            revenue=Decimal(str(row["revenue"])),
        )
        for row in rows
    ]
