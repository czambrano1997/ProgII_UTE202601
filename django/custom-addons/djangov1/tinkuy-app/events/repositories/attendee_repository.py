from __future__ import annotations

from django.db import transaction
from django.db.models import QuerySet

from events.models import Attendee, Registration

# ---------------------------------------------------------------------------
# Reads
# ---------------------------------------------------------------------------


def get_by_id(pk: int) -> Attendee | None:
    return Attendee.objects.filter(pk=pk).first()


def get_by_email(email: str) -> Attendee | None:
    return Attendee.objects.filter(email=email).first()


def list_all() -> QuerySet[Attendee]:
    return Attendee.objects.all()


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


# ---------------------------------------------------------------------------
# Writes — the only ORM write path for Attendee (ADR-0001, ADR-0006)
# ---------------------------------------------------------------------------


def create(*, full_name: str, email: str, phone: str = "", is_student: bool = False) -> Attendee:
    # atomic savepoint so a unique-email violation rolls back cleanly.
    with transaction.atomic():
        return Attendee.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            is_student=is_student,
        )


def update(
    attendee_id: int,
    *,
    full_name: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    is_student: bool | None = None,
) -> Attendee | None:
    """Partial update: only the fields passed (non-``None``) are written."""
    attendee = Attendee.objects.filter(pk=attendee_id).first()
    if attendee is None:
        return None
    if full_name is not None:
        attendee.full_name = full_name
    if email is not None:
        attendee.email = email
    if phone is not None:
        attendee.phone = phone
    if is_student is not None:
        attendee.is_student = is_student
    attendee.save()
    return attendee


def delete(attendee_id: int) -> bool:
    deleted, _ = Attendee.objects.filter(pk=attendee_id).delete()
    return deleted > 0


def get_or_create(
    *,
    email: str,
    full_name: str,
    phone: str = "",
    is_student: bool = False,
) -> tuple[Attendee, bool]:
    """Idempotent create keyed on the natural key ``email`` (seeding path)."""
    return Attendee.objects.get_or_create(
        email=email,
        defaults={
            "full_name": full_name,
            "phone": phone,
            "is_student": is_student,
        },
    )
