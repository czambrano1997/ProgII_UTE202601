# pyright: reportMissingTypeStubs=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false
"""API routing: one DRF router, one route per aggregate, mounted at ``/api/``."""
from __future__ import annotations

from rest_framework.routers import DefaultRouter

from events.api.viewsets import (
    AttendeeViewSet,
    EventViewSet,
    RegistrationViewSet,
    RoomViewSet,
    SessionViewSet,
    SpeakerViewSet,
)

router = DefaultRouter()
router.register("events", EventViewSet, basename="event")
router.register("rooms", RoomViewSet, basename="room")
router.register("speakers", SpeakerViewSet, basename="speaker")
router.register("sessions", SessionViewSet, basename="session")
router.register("attendees", AttendeeViewSet, basename="attendee")
router.register("registrations", RegistrationViewSet, basename="registration")

urlpatterns = router.urls
