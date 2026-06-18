from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from django.db.models import QuerySet

from events.models import Event
from events.repositories._sql import fetchall


def list_published() -> QuerySet[Event]:
    return Event.objects.filter(is_published=True).order_by("start_date")


def get_by_slug(slug: str) -> Event | None:
    return Event.objects.filter(slug=slug).first()


def list_all() -> QuerySet[Event]:
    return Event.objects.all()


def create(
    *,
    name: str,
    slug: str,
    summary: str,
    start_date: str,
    end_date: str,
    capacity: int,
    ticket_price: Decimal,
) -> Event:
    return Event.objects.create(
        name=name,
        slug=slug,
        summary=summary,
        start_date=start_date,
        end_date=end_date,
        capacity=capacity,
        ticket_price=ticket_price,
    )


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
