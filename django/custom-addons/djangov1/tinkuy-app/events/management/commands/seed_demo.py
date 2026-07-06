# pyright: reportMissingTypeStubs=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false
"""``manage.py seed_demo`` — fill the database with realistic demo data.

Pipeline (ADR-0006, option 1): factory_boy/Faker build attribute dicts, which
are persisted **only** through the repository ``get_or_create`` functions — the
same write seam the DRF API uses, never ``Model.objects.create`` directly.

Properties:
- **Ordered** so every FK/uniqueness dependency exists before it is referenced.
- **Idempotent** via ``get_or_create`` on the natural keys (Room.name,
  Speaker.email, Event.slug, (event, slug), Attendee.email, (attendee, session))
  plus a per-run sequence reset, so re-running converges instead of duplicating.
- **Transactional** — the whole run is wrapped in ``transaction.atomic``.
- **Deterministic** — fixed Faker / factory_boy seed.

Flags: ``--scale N`` (rows per aggregate, default 5) and ``--flush`` (clear the
seven aggregates first, through the repositories).
"""
from __future__ import annotations

from datetime import datetime, time, timedelta
from typing import Any

from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from django.utils import timezone
from faker import Faker

import factory.random

from events.management.commands._factories import (
    ALL_FACTORIES,
    AttendeeDictFactory,
    EventDictFactory,
    RegistrationDictFactory,
    RoomDictFactory,
    SessionDictFactory,
    SpeakerDictFactory,
)
from events.models import Attendee, Event, Room, Session, Speaker
from events.repositories import (
    attendee_repository,
    event_repository,
    registration_repository,
    room_repository,
    session_repository,
    speaker_repository,
)

SEED = 2026


class Command(BaseCommand):
    help = "Genera datos de demostración idempotentes a través de los repositorios."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--scale",
            type=int,
            default=5,
            help="Número de filas por agregado (por defecto 5).",
        )
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Vacía los siete agregados (vía repositorios) antes de sembrar.",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        scale: int = options["scale"]
        flush: bool = options["flush"]
        if scale < 1:
            self.stderr.write("--scale debe ser >= 1")
            return

        # Reproducible + idempotent: reset sequences and reseed every run so the
        # natural keys are identical across invocations.
        for factory_cls in ALL_FACTORIES:
            factory_cls.reset_sequence(0, force=True)
        factory.random.reseed_random(SEED)
        Faker.seed(SEED)

        with transaction.atomic():
            if flush:
                self._flush()

            rooms = self._seed_rooms(scale)
            speakers = self._seed_speakers(scale)
            events = self._seed_events(scale)
            sessions = self._seed_sessions(events, rooms, speakers, scale)
            attendees = self._seed_attendees(scale)
            registrations = self._seed_registrations(attendees, sessions)

        self.stdout.write(
            self.style.SUCCESS(
                "Sembrado completo (escala {scale}): "
                "{r} salas, {sp} ponentes, {e} eventos, {se} sesiones, "
                "{a} asistentes, {reg} registros.".format(
                    scale=scale,
                    r=len(rooms),
                    sp=len(speakers),
                    e=len(events),
                    se=len(sessions),
                    a=len(attendees),
                    reg=registrations,
                )
            )
        )

    # -- flush ---------------------------------------------------------------

    def _flush(self) -> None:
        """Delete the seven aggregates in FK-safe order, via repositories."""
        for registration in list(registration_repository.list_all()):
            registration_repository.delete(registration.id)
        for session in list(session_repository.list_all()):
            session_repository.delete(session.id)
        for attendee in list(attendee_repository.list_all()):
            attendee_repository.delete(attendee.id)
        for event in list(event_repository.list_all()):
            event_repository.delete(event.id)
        for speaker in list(speaker_repository.list_all()):
            speaker_repository.delete(speaker.id)  # cascades to SpeakerProfile
        for room in list(room_repository.list_all()):
            room_repository.delete(room.id)

    # -- per-aggregate seeders ----------------------------------------------

    def _seed_rooms(self, scale: int) -> list[Room]:
        rooms: list[Room] = []
        for _ in range(scale):
            data = RoomDictFactory.build()
            room, _created = room_repository.get_or_create(
                name=data["name"],
                floor=data["floor"],
                seating_capacity=data["seating_capacity"],
                has_projector=data["has_projector"],
                notes=data["notes"],
            )
            rooms.append(room)
        return rooms

    def _seed_speakers(self, scale: int) -> list[Speaker]:
        speakers: list[Speaker] = []
        for _ in range(scale):
            data = SpeakerDictFactory.build()
            speaker, _created = speaker_repository.get_or_create(
                email=data["email"],
                full_name=data["full_name"],
                bio=data["bio"],
                twitter_url=data["twitter_url"],
                rating=data["rating"],
                company=data["company"],
                years_experience=data["years_experience"],
                profile_website=data["profile_website"],
            )
            speakers.append(speaker)
        return speakers

    def _seed_events(self, scale: int) -> list[Event]:
        events: list[Event] = []
        for _ in range(scale):
            data = EventDictFactory.build()
            event, _created = event_repository.get_or_create(
                slug=data["slug"],
                name=data["name"],
                summary=data["summary"],
                website=data["website"],
                start_date=data["start_date"],
                end_date=data["end_date"],
                capacity=data["capacity"],
                ticket_price=data["ticket_price"],
                is_published=data["is_published"],
            )
            events.append(event)
        return events

    def _seed_sessions(
        self,
        events: list[Event],
        rooms: list[Room],
        speakers: list[Speaker],
        scale: int,
    ) -> list[Session]:
        if not rooms or not speakers:
            return []
        room_ids = [room.id for room in rooms]
        speaker_ids = [speaker.id for speaker in speakers]
        sessions: list[Session] = []
        index = 0
        for event in events:
            for slot in range(scale):
                data = SessionDictFactory.build()
                hour = 9 + (slot % 8)  # 09:00–16:00
                start_time = time(hour, 0)
                scheduled_at = timezone.make_aware(
                    datetime.combine(event.start_date, start_time)
                )
                chosen = [
                    speaker_ids[index % len(speaker_ids)],
                    speaker_ids[(index + 1) % len(speaker_ids)],
                ]
                session, _created = session_repository.get_or_create(
                    event_id=event.id,
                    slug=data["slug"],
                    room_id=room_ids[index % len(room_ids)],
                    title=data["title"],
                    abstract=data["abstract"],
                    level=data["level"],
                    scheduled_at=scheduled_at,
                    start_time=start_time,
                    duration=timedelta(minutes=45),
                    max_seats=data["max_seats"],
                    speaker_ids=chosen,
                    is_keynote=data["is_keynote"],
                )
                sessions.append(session)
                index += 1
        return sessions

    def _seed_attendees(self, scale: int) -> list[Attendee]:
        attendees: list[Attendee] = []
        for _ in range(scale):
            data = AttendeeDictFactory.build()
            attendee, _created = attendee_repository.get_or_create(
                email=data["email"],
                full_name=data["full_name"],
                phone=data["phone"],
                is_student=data["is_student"],
            )
            attendees.append(attendee)
        return attendees

    def _seed_registrations(
        self, attendees: list[Attendee], sessions: list[Session]
    ) -> int:
        if not sessions:
            return 0
        count = 0
        for position, attendee in enumerate(attendees):
            for offset in range(2):  # two sessions per attendee
                session = sessions[(position + offset) % len(sessions)]
                data = RegistrationDictFactory.build()
                registration_repository.get_or_create(
                    attendee_id=attendee.id,
                    session_id=session.id,
                    confirmed=data["confirmed"],
                    seat_number=data["seat_number"],
                    amount_paid=data["amount_paid"],
                )
                count += 1
        return count
