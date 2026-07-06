from __future__ import annotations

from dataclasses import dataclass

from django.db import transaction
from django.db.models import QuerySet

from events.models import Speaker, SpeakerProfile
from events.repositories._sql import fetchall

# ---------------------------------------------------------------------------
# Reads
# ---------------------------------------------------------------------------


def list_all() -> QuerySet[Speaker]:
    return Speaker.objects.all()


def get_by_id(pk: int) -> Speaker | None:
    return Speaker.objects.filter(pk=pk).first()


def get_by_email(email: str) -> Speaker | None:
    return Speaker.objects.filter(email=email).first()


def get_profile(speaker_id: int) -> SpeakerProfile | None:
    return SpeakerProfile.objects.filter(speaker_id=speaker_id).first()


# ---------------------------------------------------------------------------
# Writes — the only ORM write path for Speaker / SpeakerProfile.
# The optional 1:1 profile is created in the same transaction (ADR-0006).
# ---------------------------------------------------------------------------


def create(
    *,
    full_name: str,
    email: str,
    bio: str,
    twitter_url: str = "",
    rating: float = 0.0,
    company: str | None = None,
    years_experience: int | None = None,
    profile_website: str | None = None,
) -> Speaker:
    with transaction.atomic():
        speaker = Speaker.objects.create(
            full_name=full_name,
            email=email,
            bio=bio,
            twitter_url=twitter_url,
            rating=rating,
        )
        if company is not None or years_experience is not None or profile_website is not None:
            SpeakerProfile.objects.create(
                speaker=speaker,
                company=company or "",
                years_experience=years_experience or 0,
                website=profile_website or "",
            )
        return speaker


def update(
    speaker_id: int,
    *,
    full_name: str | None = None,
    email: str | None = None,
    bio: str | None = None,
    twitter_url: str | None = None,
    rating: float | None = None,
    company: str | None = None,
    years_experience: int | None = None,
    profile_website: str | None = None,
) -> Speaker | None:
    """Partial update. Profile fields upsert the 1:1 ``SpeakerProfile``."""
    with transaction.atomic():
        speaker = Speaker.objects.filter(pk=speaker_id).first()
        if speaker is None:
            return None
        if full_name is not None:
            speaker.full_name = full_name
        if email is not None:
            speaker.email = email
        if bio is not None:
            speaker.bio = bio
        if twitter_url is not None:
            speaker.twitter_url = twitter_url
        if rating is not None:
            speaker.rating = rating
        speaker.save()
        if company is not None or years_experience is not None or profile_website is not None:
            profile = SpeakerProfile.objects.filter(speaker_id=speaker_id).first()
            if profile is None:
                profile = SpeakerProfile(speaker=speaker)
            if company is not None:
                profile.company = company
            if years_experience is not None:
                profile.years_experience = years_experience
            if profile_website is not None:
                profile.website = profile_website
            profile.save()
        return speaker


def delete(speaker_id: int) -> bool:
    deleted, _ = Speaker.objects.filter(pk=speaker_id).delete()
    return deleted > 0


def get_or_create(
    *,
    email: str,
    full_name: str,
    bio: str,
    twitter_url: str = "",
    rating: float = 0.0,
    company: str = "",
    years_experience: int = 0,
    profile_website: str = "",
) -> tuple[Speaker, bool]:
    """Idempotent create keyed on the natural key ``email`` (seeding path)."""
    with transaction.atomic():
        speaker, created = Speaker.objects.get_or_create(
            email=email,
            defaults={
                "full_name": full_name,
                "bio": bio,
                "twitter_url": twitter_url,
                "rating": rating,
            },
        )
        if created:
            SpeakerProfile.objects.get_or_create(
                speaker=speaker,
                defaults={
                    "company": company,
                    "years_experience": years_experience,
                    "website": profile_website,
                },
            )
        return speaker, created


# ---------------------------------------------------------------------------
# Reports (raw SQL → DTOs)
# ---------------------------------------------------------------------------


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
