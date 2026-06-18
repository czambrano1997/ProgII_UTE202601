"""Integration tests for ORM repository functions.

These tests require a database (pytest-django creates a test DB automatically).
They exercise the repository layer without touching views.
"""
from __future__ import annotations

import datetime
from decimal import Decimal

import pytest

from events.models import Attendee, Event, Room, Session, Speaker


@pytest.mark.django_db
class TestEventRepository:
    def _make_event(self, *, published: bool = True) -> Event:
        return Event.objects.create(
            name="PyCon Ecuador",
            slug="pycon-ecuador",
            summary="La conferencia de Python del Ecuador.",
            start_date=datetime.date(2025, 9, 1),
            end_date=datetime.date(2025, 9, 3),
            capacity=300,
            ticket_price=Decimal("25.00"),
            is_published=published,
        )

    def test_list_published_returns_only_published(self) -> None:
        from events.repositories import event_repository

        self._make_event(published=True)
        self._make_event.__func__  # type: ignore[attr-defined]
        Event.objects.create(
            name="Evento privado",
            slug="evento-privado",
            summary="Oculto",
            start_date=datetime.date(2025, 10, 1),
            end_date=datetime.date(2025, 10, 2),
            capacity=50,
            ticket_price=Decimal("0"),
            is_published=False,
        )
        qs = event_repository.list_published()
        assert qs.count() == 1
        assert qs.first().name == "PyCon Ecuador"  # type: ignore[union-attr]

    def test_get_by_slug_found(self) -> None:
        from events.repositories import event_repository

        self._make_event()
        event = event_repository.get_by_slug("pycon-ecuador")
        assert event is not None
        assert event.name == "PyCon Ecuador"

    def test_get_by_slug_not_found(self) -> None:
        from events.repositories import event_repository

        result = event_repository.get_by_slug("no-existe")
        assert result is None


@pytest.mark.django_db
class TestAttendeeRepository:
    def test_create_and_retrieve(self) -> None:
        from events.repositories import attendee_repository

        attendee = attendee_repository.create(
            full_name="Ana Torres",
            email="ana@ute.edu.ec",
            is_student=True,
        )
        assert attendee.pk is not None
        fetched = attendee_repository.get_by_id(attendee.pk)
        assert fetched is not None
        assert fetched.full_name == "Ana Torres"

    def test_list_students_excludes_non_students(self) -> None:
        from events.repositories import attendee_repository

        attendee_repository.create(full_name="Est.", email="est@ute.edu.ec", is_student=True)
        attendee_repository.create(full_name="Prof.", email="prof@ute.edu.ec", is_student=False)
        students = attendee_repository.list_students()
        assert students.count() == 1
        assert students.first().email == "est@ute.edu.ec"  # type: ignore[union-attr]

    def test_get_by_id_missing_returns_none(self) -> None:
        from events.repositories import attendee_repository

        assert attendee_repository.get_by_id(99999) is None


@pytest.mark.django_db
class TestSpeakerRepository:
    def test_get_by_id(self) -> None:
        from events.repositories import speaker_repository

        sp = Speaker.objects.create(
            full_name="Carlos Mendoza",
            email="carlos@tinkuy.ec",
            bio="Experto en Python.",
        )
        found = speaker_repository.get_by_id(sp.pk)
        assert found is not None
        assert found.full_name == "Carlos Mendoza"

    def test_get_profile_none_when_no_profile(self) -> None:
        from events.repositories import speaker_repository

        sp = Speaker.objects.create(
            full_name="Sin Perfil",
            email="sinperfil@tinkuy.ec",
            bio="Bio.",
        )
        assert speaker_repository.get_profile(sp.pk) is None


@pytest.mark.django_db
class TestSessionRepository:
    def _make_event(self) -> Event:
        return Event.objects.create(
            name="DjangoCon",
            slug="djangocon",
            summary="Django conference.",
            start_date=datetime.date(2025, 11, 1),
            end_date=datetime.date(2025, 11, 2),
            capacity=200,
            ticket_price=Decimal("15.00"),
        )

    def _make_room(self) -> Room:
        return Room.objects.create(name="Aula Magna", floor=1, seating_capacity=200)

    def test_list_by_event_returns_sessions(self) -> None:
        from events.repositories import session_repository

        event = self._make_event()
        room = self._make_room()
        Session.objects.create(
            event=event,
            room=room,
            title="Intro a Django",
            slug="intro-django",
            abstract="ABC",
            level="beginner",
            scheduled_at=datetime.datetime(2025, 11, 1, 9, 0, tzinfo=datetime.timezone.utc),
            start_time=datetime.time(9, 0),
            duration=datetime.timedelta(hours=1),
            max_seats=100,
        )
        sessions = session_repository.list_by_event(event.pk)
        assert sessions.count() == 1

    def test_get_by_slug_not_found(self) -> None:
        from events.repositories import session_repository

        result = session_repository.get_by_slug(9999, "no-slug")
        assert result is None
