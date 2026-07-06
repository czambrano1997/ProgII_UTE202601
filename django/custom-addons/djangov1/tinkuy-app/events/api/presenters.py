"""Output mapping: typed model instances -> plain JSON-ready dicts.

These helpers stay free of DRF so they remain fully ``pyright`` strict. The
returned values use native Python types (``date``, ``datetime``, ``Decimal``,
``timedelta``); DRF's ``JSONRenderer`` encodes them on the way out.
"""
from __future__ import annotations

from events.models import Attendee, Event, Registration, Room, Session, Speaker, SpeakerProfile


def event_to_dict(event: Event) -> dict[str, object]:
    return {
        "id": event.id,
        "name": event.name,
        "slug": event.slug,
        "summary": event.summary,
        "website": event.website,
        "start_date": event.start_date,
        "end_date": event.end_date,
        "is_published": event.is_published,
        "capacity": event.capacity,
        "ticket_price": event.ticket_price,
        "created_at": event.created_at,
    }


def room_to_dict(room: Room) -> dict[str, object]:
    return {
        "id": room.id,
        "name": room.name,
        "floor": room.floor,
        "seating_capacity": room.seating_capacity,
        "has_projector": room.has_projector,
        "notes": room.notes,
    }


def speaker_to_dict(speaker: Speaker, profile: SpeakerProfile | None) -> dict[str, object]:
    return {
        "id": speaker.id,
        "full_name": speaker.full_name,
        "email": speaker.email,
        "bio": speaker.bio,
        "twitter_url": speaker.twitter_url,
        "rating": speaker.rating,
        "profile": (
            {
                "company": profile.company,
                "years_experience": profile.years_experience,
                "website": profile.website,
            }
            if profile is not None
            else None
        ),
    }


def session_to_dict(session: Session) -> dict[str, object]:
    return {
        "id": session.id,
        "event": session.event_id,
        "room": session.room_id,
        "speakers": [speaker.id for speaker in session.speakers.all()],
        "title": session.title,
        "slug": session.slug,
        "abstract": session.abstract,
        "level": session.level,
        "scheduled_at": session.scheduled_at,
        "start_time": session.start_time,
        "duration": session.duration,
        "is_keynote": session.is_keynote,
        "max_seats": session.max_seats,
        "recording_url": session.recording_url,
    }


def attendee_to_dict(attendee: Attendee) -> dict[str, object]:
    return {
        "id": attendee.id,
        "full_name": attendee.full_name,
        "email": attendee.email,
        "phone": attendee.phone,
        "registered_on": attendee.registered_on,
        "is_student": attendee.is_student,
    }


def registration_to_dict(registration: Registration) -> dict[str, object]:
    return {
        "id": registration.id,
        "attendee": registration.attendee_id,
        "session": registration.session_id,
        "confirmed": registration.confirmed,
        "seat_number": registration.seat_number,
        "amount_paid": registration.amount_paid,
        "created_at": registration.created_at,
    }
