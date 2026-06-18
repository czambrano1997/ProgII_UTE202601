"""View tests using Django's test client — require database."""
from __future__ import annotations

import datetime
from decimal import Decimal

import pytest
from django.test import Client


@pytest.fixture
def client() -> Client:
    return Client()


@pytest.mark.django_db
class TestEventViews:
    def _make_event(self, *, published: bool = True) -> None:
        from events.models import Event

        Event.objects.create(
            name="PyCon EC",
            slug="pycon-ec",
            summary="La conferencia.",
            start_date=datetime.date(2025, 9, 1),
            end_date=datetime.date(2025, 9, 3),
            capacity=300,
            ticket_price=Decimal("25.00"),
            is_published=published,
        )

    def test_event_list_ok(self, client: Client) -> None:
        self._make_event()
        response = client.get("/")
        assert response.status_code == 200

    def test_event_detail_ok(self, client: Client) -> None:
        self._make_event()
        response = client.get("/eventos/pycon-ec/")
        assert response.status_code == 200

    def test_event_detail_404(self, client: Client) -> None:
        response = client.get("/eventos/no-existe/")
        assert response.status_code == 404

    def test_event_poster_ok(self, client: Client) -> None:
        self._make_event()
        response = client.get("/eventos/pycon-ec/poster/")
        assert response.status_code == 200

    def test_lineup_poster_ok(self, client: Client) -> None:
        self._make_event()
        response = client.get("/eventos/pycon-ec/lineup/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestSpeakerViews:
    def test_speaker_list_empty(self, client: Client) -> None:
        response = client.get("/ponentes/")
        assert response.status_code == 200

    def test_speaker_detail_404(self, client: Client) -> None:
        response = client.get("/ponentes/9999/")
        assert response.status_code == 404


@pytest.mark.django_db
class TestRoomViews:
    def test_room_list_empty(self, client: Client) -> None:
        response = client.get("/salas/")
        assert response.status_code == 200

    def test_room_detail_404(self, client: Client) -> None:
        response = client.get("/salas/9999/")
        assert response.status_code == 404


@pytest.mark.django_db
class TestAttendeeViews:
    def test_attendee_list_empty(self, client: Client) -> None:
        response = client.get("/asistentes/")
        assert response.status_code == 200

    def test_attendee_detail_404(self, client: Client) -> None:
        response = client.get("/asistentes/9999/")
        assert response.status_code == 404
