# pyright: reportMissingTypeStubs=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUntypedBaseClass=false, reportUnknownArgumentType=false, reportUnknownParameterType=false, reportMissingParameterType=false
"""DRF ViewSets — the HTTP surface for CRUD over the seven aggregates.

Every handler is thin: validate with an input serializer, call a repository
read/write function, and present the result with ``events.api.presenters``. No
ORM access and no business logic live here, mirroring how the template views
delegate reads today (ADR-0003/ADR-0006).

Plain ``viewsets.ViewSet`` is used rather than ``ModelViewSet`` precisely so the
ORM is reached only through the repository seam.
"""
from __future__ import annotations

from typing import Any

from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from events.api import presenters
from events.api.serializers import (
    AttendeeInSerializer,
    EventInSerializer,
    RegistrationInSerializer,
    RoomInSerializer,
    SessionInSerializer,
    SpeakerInSerializer,
)
from events.repositories import (
    attendee_repository,
    event_repository,
    registration_repository,
    room_repository,
    session_repository,
    speaker_repository,
)


def _require_pk(pk: str | None) -> int:
    if pk is None or not pk.isdigit():
        raise Http404
    return int(pk)


def _validated(serializer_cls: Any, request: Request, *, partial: bool) -> dict[str, Any]:
    serializer = serializer_cls(data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data


class EventViewSet(viewsets.ViewSet):
    serializer_class = EventInSerializer

    def list(self, request: Request) -> Response:
        return Response([presenters.event_to_dict(e) for e in event_repository.list_all()])

    def retrieve(self, request: Request, pk: str | None = None) -> Response:
        event = event_repository.get_by_id(_require_pk(pk))
        if event is None:
            raise Http404
        return Response(presenters.event_to_dict(event))

    def create(self, request: Request) -> Response:
        data = _validated(EventInSerializer, request, partial=False)
        event = event_repository.create(
            name=data["name"],
            slug=data["slug"],
            summary=data["summary"],
            website=data["website"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            is_published=data["is_published"],
            capacity=data["capacity"],
            ticket_price=data["ticket_price"],
        )
        return Response(presenters.event_to_dict(event), status=status.HTTP_201_CREATED)

    def update(self, request: Request, pk: str | None = None) -> Response:
        return self._apply_update(request, pk, partial=False)

    def partial_update(self, request: Request, pk: str | None = None) -> Response:
        return self._apply_update(request, pk, partial=True)

    def _apply_update(self, request: Request, pk: str | None, *, partial: bool) -> Response:
        data = _validated(EventInSerializer, request, partial=partial)
        event = event_repository.update(
            _require_pk(pk),
            name=data.get("name"),
            slug=data.get("slug"),
            summary=data.get("summary"),
            website=data.get("website"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            is_published=data.get("is_published"),
            capacity=data.get("capacity"),
            ticket_price=data.get("ticket_price"),
        )
        if event is None:
            raise Http404
        return Response(presenters.event_to_dict(event))

    def destroy(self, request: Request, pk: str | None = None) -> Response:
        if not event_repository.delete(_require_pk(pk)):
            raise Http404
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomViewSet(viewsets.ViewSet):
    serializer_class = RoomInSerializer

    def list(self, request: Request) -> Response:
        return Response([presenters.room_to_dict(r) for r in room_repository.list_all()])

    def retrieve(self, request: Request, pk: str | None = None) -> Response:
        room = room_repository.get_by_id(_require_pk(pk))
        if room is None:
            raise Http404
        return Response(presenters.room_to_dict(room))

    def create(self, request: Request) -> Response:
        data = _validated(RoomInSerializer, request, partial=False)
        room = room_repository.create(
            name=data["name"],
            floor=data["floor"],
            seating_capacity=data["seating_capacity"],
            has_projector=data["has_projector"],
            notes=data["notes"],
        )
        return Response(presenters.room_to_dict(room), status=status.HTTP_201_CREATED)

    def update(self, request: Request, pk: str | None = None) -> Response:
        return self._apply_update(request, pk, partial=False)

    def partial_update(self, request: Request, pk: str | None = None) -> Response:
        return self._apply_update(request, pk, partial=True)

    def _apply_update(self, request: Request, pk: str | None, *, partial: bool) -> Response:
        data = _validated(RoomInSerializer, request, partial=partial)
        room = room_repository.update(
            _require_pk(pk),
            name=data.get("name"),
            floor=data.get("floor"),
            seating_capacity=data.get("seating_capacity"),
            has_projector=data.get("has_projector"),
            notes=data.get("notes"),
        )
        if room is None:
            raise Http404
        return Response(presenters.room_to_dict(room))

    def destroy(self, request: Request, pk: str | None = None) -> Response:
        if not room_repository.delete(_require_pk(pk)):
            raise Http404
        return Response(status=status.HTTP_204_NO_CONTENT)


class SpeakerViewSet(viewsets.ViewSet):
    serializer_class = SpeakerInSerializer

    def list(self, request: Request) -> Response:
        return Response(
            [
                presenters.speaker_to_dict(s, speaker_repository.get_profile(s.id))
                for s in speaker_repository.list_all()
            ]
        )

    def retrieve(self, request: Request, pk: str | None = None) -> Response:
        speaker = speaker_repository.get_by_id(_require_pk(pk))
        if speaker is None:
            raise Http404
        return Response(
            presenters.speaker_to_dict(speaker, speaker_repository.get_profile(speaker.id))
        )

    def create(self, request: Request) -> Response:
        data = _validated(SpeakerInSerializer, request, partial=False)
        speaker = speaker_repository.create(
            full_name=data["full_name"],
            email=data["email"],
            bio=data["bio"],
            twitter_url=data["twitter_url"],
            rating=data["rating"],
            company=data["company"],
            years_experience=data["years_experience"],
            profile_website=data["profile_website"],
        )
        return Response(
            presenters.speaker_to_dict(speaker, speaker_repository.get_profile(speaker.id)),
            status=status.HTTP_201_CREATED,
        )

    def update(self, request: Request, pk: str | None = None) -> Response:
        return self._apply_update(request, pk, partial=False)

    def partial_update(self, request: Request, pk: str | None = None) -> Response:
        return self._apply_update(request, pk, partial=True)

    def _apply_update(self, request: Request, pk: str | None, *, partial: bool) -> Response:
        data = _validated(SpeakerInSerializer, request, partial=partial)
        speaker = speaker_repository.update(
            _require_pk(pk),
            full_name=data.get("full_name"),
            email=data.get("email"),
            bio=data.get("bio"),
            twitter_url=data.get("twitter_url"),
            rating=data.get("rating"),
            company=data.get("company"),
            years_experience=data.get("years_experience"),
            profile_website=data.get("profile_website"),
        )
        if speaker is None:
            raise Http404
        return Response(
            presenters.speaker_to_dict(speaker, speaker_repository.get_profile(speaker.id))
        )

    def destroy(self, request: Request, pk: str | None = None) -> Response:
        if not speaker_repository.delete(_require_pk(pk)):
            raise Http404
        return Response(status=status.HTTP_204_NO_CONTENT)


class SessionViewSet(viewsets.ViewSet):
    serializer_class = SessionInSerializer

    def list(self, request: Request) -> Response:
        return Response([presenters.session_to_dict(s) for s in session_repository.list_all()])

    def retrieve(self, request: Request, pk: str | None = None) -> Response:
        session = session_repository.get_by_id(_require_pk(pk))
        if session is None:
            raise Http404
        return Response(presenters.session_to_dict(session))

    def create(self, request: Request) -> Response:
        data = _validated(SessionInSerializer, request, partial=False)
        session = session_repository.create(
            event_id=data["event"],
            room_id=data["room"],
            speaker_ids=data["speakers"],
            title=data["title"],
            slug=data["slug"],
            abstract=data["abstract"],
            level=data["level"],
            scheduled_at=data["scheduled_at"],
            start_time=data["start_time"],
            duration=data["duration"],
            is_keynote=data["is_keynote"],
            max_seats=data["max_seats"],
            recording_url=data["recording_url"],
        )
        return Response(presenters.session_to_dict(session), status=status.HTTP_201_CREATED)

    def update(self, request: Request, pk: str | None = None) -> Response:
        return self._apply_update(request, pk, partial=False)

    def partial_update(self, request: Request, pk: str | None = None) -> Response:
        return self._apply_update(request, pk, partial=True)

    def _apply_update(self, request: Request, pk: str | None, *, partial: bool) -> Response:
        data = _validated(SessionInSerializer, request, partial=partial)
        session = session_repository.update(
            _require_pk(pk),
            room_id=data.get("room"),
            speaker_ids=data.get("speakers"),
            title=data.get("title"),
            slug=data.get("slug"),
            abstract=data.get("abstract"),
            level=data.get("level"),
            scheduled_at=data.get("scheduled_at"),
            start_time=data.get("start_time"),
            duration=data.get("duration"),
            is_keynote=data.get("is_keynote"),
            max_seats=data.get("max_seats"),
            recording_url=data.get("recording_url"),
        )
        if session is None:
            raise Http404
        return Response(presenters.session_to_dict(session))

    def destroy(self, request: Request, pk: str | None = None) -> Response:
        if not session_repository.delete(_require_pk(pk)):
            raise Http404
        return Response(status=status.HTTP_204_NO_CONTENT)


class AttendeeViewSet(viewsets.ViewSet):
    serializer_class = AttendeeInSerializer

    def list(self, request: Request) -> Response:
        return Response([presenters.attendee_to_dict(a) for a in attendee_repository.list_all()])

    def retrieve(self, request: Request, pk: str | None = None) -> Response:
        attendee = attendee_repository.get_by_id(_require_pk(pk))
        if attendee is None:
            raise Http404
        return Response(presenters.attendee_to_dict(attendee))

    def create(self, request: Request) -> Response:
        data = _validated(AttendeeInSerializer, request, partial=False)
        attendee = attendee_repository.create(
            full_name=data["full_name"],
            email=data["email"],
            phone=data["phone"],
            is_student=data["is_student"],
        )
        return Response(presenters.attendee_to_dict(attendee), status=status.HTTP_201_CREATED)

    def update(self, request: Request, pk: str | None = None) -> Response:
        return self._apply_update(request, pk, partial=False)

    def partial_update(self, request: Request, pk: str | None = None) -> Response:
        return self._apply_update(request, pk, partial=True)

    def _apply_update(self, request: Request, pk: str | None, *, partial: bool) -> Response:
        data = _validated(AttendeeInSerializer, request, partial=partial)
        attendee = attendee_repository.update(
            _require_pk(pk),
            full_name=data.get("full_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            is_student=data.get("is_student"),
        )
        if attendee is None:
            raise Http404
        return Response(presenters.attendee_to_dict(attendee))

    def destroy(self, request: Request, pk: str | None = None) -> Response:
        if not attendee_repository.delete(_require_pk(pk)):
            raise Http404
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegistrationViewSet(viewsets.ViewSet):
    serializer_class = RegistrationInSerializer

    def list(self, request: Request) -> Response:
        return Response(
            [presenters.registration_to_dict(r) for r in registration_repository.list_all()]
        )

    def retrieve(self, request: Request, pk: str | None = None) -> Response:
        registration = registration_repository.get_by_id(_require_pk(pk))
        if registration is None:
            raise Http404
        return Response(presenters.registration_to_dict(registration))

    def create(self, request: Request) -> Response:
        data = _validated(RegistrationInSerializer, request, partial=False)
        registration = registration_repository.create(
            attendee_id=data["attendee"],
            session_id=data["session"],
            confirmed=data["confirmed"],
            seat_number=data["seat_number"],
            amount_paid=data["amount_paid"],
        )
        return Response(
            presenters.registration_to_dict(registration), status=status.HTTP_201_CREATED
        )

    def update(self, request: Request, pk: str | None = None) -> Response:
        return self._apply_update(request, pk, partial=False)

    def partial_update(self, request: Request, pk: str | None = None) -> Response:
        return self._apply_update(request, pk, partial=True)

    def _apply_update(self, request: Request, pk: str | None, *, partial: bool) -> Response:
        data = _validated(RegistrationInSerializer, request, partial=partial)
        registration = registration_repository.update(
            _require_pk(pk),
            confirmed=data.get("confirmed"),
            seat_number=data.get("seat_number"),
            amount_paid=data.get("amount_paid"),
        )
        if registration is None:
            raise Http404
        return Response(presenters.registration_to_dict(registration))

    def destroy(self, request: Request, pk: str | None = None) -> Response:
        if not registration_repository.delete(_require_pk(pk)):
            raise Http404
        return Response(status=status.HTTP_204_NO_CONTENT)
