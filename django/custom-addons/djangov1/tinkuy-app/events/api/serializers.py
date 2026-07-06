# pyright: reportMissingTypeStubs=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUntypedBaseClass=false, reportUnknownArgumentType=false
"""DRF input serializers (validation only).

These validate and coerce incoming JSON. They are deliberately **not**
``ModelSerializer`` subclasses: ModelSerializer reads and writes the ORM
directly, which would bypass the repository write seam (ADR-0001/ADR-0006).
Output is handled by ``events.api.presenters`` instead, so nothing here ever
touches the database.

For updates the same serializer is instantiated with ``partial=True`` so only
the supplied fields land in ``validated_data`` — a clean match for the
repositories' partial ``update`` functions.
"""
from __future__ import annotations

from decimal import Decimal

from rest_framework import serializers

from events.models import Level


class EventInSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    slug = serializers.SlugField()
    summary = serializers.CharField()
    website = serializers.URLField(required=False, allow_blank=True, default="")
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    is_published = serializers.BooleanField(required=False, default=False)
    capacity = serializers.IntegerField(min_value=0)
    ticket_price = serializers.DecimalField(max_digits=8, decimal_places=2)


class RoomInSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    floor = serializers.IntegerField()
    seating_capacity = serializers.IntegerField(min_value=0)
    has_projector = serializers.BooleanField(required=False, default=True)
    notes = serializers.CharField(required=False, allow_blank=True, default="")


class SpeakerInSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    bio = serializers.CharField()
    twitter_url = serializers.URLField(required=False, allow_blank=True, default="")
    rating = serializers.FloatField(required=False, default=0.0)
    # Optional 1:1 profile fields — when present, the repository upserts the profile.
    company = serializers.CharField(max_length=200, required=False, allow_blank=True, default="")
    years_experience = serializers.IntegerField(min_value=0, required=False, default=0)
    profile_website = serializers.URLField(required=False, allow_blank=True, default="")


class SessionInSerializer(serializers.Serializer):
    event = serializers.IntegerField(min_value=1)
    room = serializers.IntegerField(min_value=1)
    speakers = serializers.ListField(
        child=serializers.IntegerField(min_value=1), required=False, default=list
    )
    title = serializers.CharField(max_length=300)
    slug = serializers.SlugField()
    abstract = serializers.CharField()
    level = serializers.ChoiceField(choices=Level.choices)
    scheduled_at = serializers.DateTimeField()
    start_time = serializers.TimeField()
    duration = serializers.DurationField()
    is_keynote = serializers.BooleanField(required=False, default=False)
    max_seats = serializers.IntegerField(min_value=0)
    recording_url = serializers.URLField(required=False, allow_blank=True, default="")


class AttendeeInSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True, default="")
    is_student = serializers.BooleanField(required=False, default=False)


class RegistrationInSerializer(serializers.Serializer):
    attendee = serializers.IntegerField(min_value=1)
    session = serializers.IntegerField(min_value=1)
    confirmed = serializers.BooleanField(required=False, default=False)
    seat_number = serializers.IntegerField(min_value=1, required=False, allow_null=True, default=None)
    amount_paid = serializers.DecimalField(
        max_digits=8, decimal_places=2, required=False, default=Decimal("0")
    )
