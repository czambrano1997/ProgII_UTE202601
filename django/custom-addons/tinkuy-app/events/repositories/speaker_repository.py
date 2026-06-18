from __future__ import annotations

from dataclasses import dataclass

from django.db.models import QuerySet

from events.models import Speaker, SpeakerProfile
from events.repositories._sql import fetchall


def list_all() -> QuerySet[Speaker]:
    return Speaker.objects.all()


def get_by_id(pk: int) -> Speaker | None:
    return Speaker.objects.filter(pk=pk).first()


def get_by_email(email: str) -> Speaker | None:
    return Speaker.objects.filter(email=email).first()


def get_profile(speaker_id: int) -> SpeakerProfile | None:
    return SpeakerProfile.objects.filter(speaker_id=speaker_id).first()


@dataclass(frozen=True)
class SpeakerSessionLoadRow:
    speaker_id: int
    full_name: str
    email: str
    session_count: int


def session_load() -> list[SpeakerSessionLoadRow]:
    rows = fetchall(
        """
        SELECT sp.id          AS speaker_id,
               sp.full_name   AS full_name,
               sp.email       AS email,
               COUNT(ss.session_id) AS session_count
        FROM events_speaker sp
        LEFT JOIN events_session_speakers ss ON ss.speaker_id = sp.id
        GROUP BY sp.id, sp.full_name, sp.email
        ORDER BY session_count DESC, sp.full_name
        """
    )
    return [
        SpeakerSessionLoadRow(
            speaker_id=int(row["speaker_id"]),
            full_name=str(row["full_name"]),
            email=str(row["email"]),
            session_count=int(row["session_count"]),
        )
        for row in rows
    ]


@dataclass(frozen=True)
class SpeakerRatingRow:
    speaker_id: int
    full_name: str
    rating: float
    session_count: int


def top_rated(limit: int = 10) -> list[SpeakerRatingRow]:
    rows = fetchall(
        """
        SELECT sp.id        AS speaker_id,
               sp.full_name AS full_name,
               sp.rating    AS rating,
               COUNT(ss.session_id) AS session_count
        FROM events_speaker sp
        LEFT JOIN events_session_speakers ss ON ss.speaker_id = sp.id
        GROUP BY sp.id, sp.full_name, sp.rating
        ORDER BY sp.rating DESC
        LIMIT %s
        """,
        (limit,),
    )
    return [
        SpeakerRatingRow(
            speaker_id=int(row["speaker_id"]),
            full_name=str(row["full_name"]),
            rating=float(row["rating"]),
            session_count=int(row["session_count"]),
        )
        for row in rows
    ]
