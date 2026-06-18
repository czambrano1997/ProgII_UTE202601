from __future__ import annotations

from django.db.models import QuerySet

from events.models import Attendee, Registration


def get_by_id(pk: int) -> Attendee | None:
    return Attendee.objects.filter(pk=pk).first()


def get_by_email(email: str) -> Attendee | None:
    return Attendee.objects.filter(email=email).first()


def list_by_session(session_id: int) -> QuerySet[Attendee]:
    return Attendee.objects.filter(
        registrations__session_id=session_id
    ).distinct()


def list_students() -> QuerySet[Attendee]:
    return Attendee.objects.filter(is_student=True).order_by("full_name")


def list_registrations(attendee_id: int) -> QuerySet[Registration]:
    return (
        Registration.objects.filter(attendee_id=attendee_id)
        .select_related("session", "session__event", "session__room")
        .order_by("-created_at")
    )


def create(*, full_name: str, email: str, phone: str = "", is_student: bool = False) -> Attendee:
    return Attendee.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        is_student=is_student,
    )
