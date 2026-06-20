from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from django.db.models import QuerySet

from events.models import Registration
from events.repositories._sql import fetchall


def list_by_attendee(attendee_id: int) -> QuerySet[Registration]:
    return (
        Registration.objects.filter(attendee_id=attendee_id)
        .select_related("session", "session__event", "session__room")
        .order_by("-created_at")
    )


def list_by_session(session_id: int) -> QuerySet[Registration]:
    return Registration.objects.filter(session_id=session_id).select_related("attendee")


def confirm(registration_id: int) -> bool:
    updated = Registration.objects.filter(pk=registration_id, confirmed=False).update(confirmed=True)
    return updated > 0


@dataclass(frozen=True)
class RoomUtilizationRow:
    room_id: int
    room_name: str
    floor: int
    session_count: int
    total_minutes: int


def room_utilization() -> list[RoomUtilizationRow]:
    rows = fetchall(
        """
        SELECT r.id                                      AS room_id,
               r.name                                    AS room_name,
               r.floor                                   AS floor,
               COUNT(s.id)                               AS session_count,
               COALESCE(
                   SUM(EXTRACT(EPOCH FROM s.duration) / 60),
                   0
               )::int                                    AS total_minutes
        FROM events_room r
        LEFT JOIN events_session s ON s.room_id = r.id
        GROUP BY r.id, r.name, r.floor
        ORDER BY total_minutes DESC
        """
    )
    return [
        RoomUtilizationRow(
            room_id=int(row["room_id"]),
            room_name=str(row["room_name"]),
            floor=int(row["floor"]),
            session_count=int(row["session_count"]),
            total_minutes=int(row["total_minutes"]),
        )
        for row in rows
    ]


@dataclass(frozen=True)
class RevenueByEventRow:
    event_id: int
    event_name: str
    confirmed_registrations: int
    total_revenue: Decimal


def revenue_by_event(event_id: int) -> list[RevenueByEventRow]:
    rows = fetchall(
        """
        SELECT e.id                              AS event_id,
               e.name                            AS event_name,
               COUNT(r.id) FILTER (WHERE r.confirmed) AS confirmed_registrations,
               COALESCE(SUM(r.amount_paid) FILTER (WHERE r.confirmed), 0) AS total_revenue
        FROM events_event e
        LEFT JOIN events_session s      ON s.event_id = e.id
        LEFT JOIN events_registration r ON r.session_id = s.id
        WHERE e.id = %s
        GROUP BY e.id, e.name
        """,
        (event_id,),
    )
    return [
        RevenueByEventRow(
            event_id=int(row["event_id"]),
            event_name=str(row["event_name"]),
            confirmed_registrations=int(row["confirmed_registrations"]),
            total_revenue=Decimal(str(row["total_revenue"])),
        )
        for row in rows
    ]
