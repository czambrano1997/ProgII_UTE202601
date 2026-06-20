from __future__ import annotations

from django.urls import path

from events.views import (
    attendee_views,
    event_views,
    poster_views,
    registration_views,
    room_views,
    session_views,
    speaker_views,
)

app_name = "events"

urlpatterns = [
    # Events
    path("", event_views.event_list, name="event_list"),
    path("eventos/<slug:slug>/", event_views.event_detail, name="event_detail"),
    # Sessions
    path("eventos/<int:event_id>/sesiones/", session_views.session_list, name="session_list"),
    path("eventos/<int:event_id>/sesiones/<slug:slug>/", session_views.session_detail, name="session_detail"),
    # Speakers
    path("ponentes/", speaker_views.speaker_list, name="speaker_list"),
    path("ponentes/<int:pk>/", speaker_views.speaker_detail, name="speaker_detail"),
    # Rooms
    path("salas/", room_views.room_list, name="room_list"),
    path("salas/<int:pk>/", room_views.room_detail, name="room_detail"),
    # Attendees
    path("asistentes/", attendee_views.attendee_list, name="attendee_list"),
    path("asistentes/<int:pk>/", attendee_views.attendee_detail, name="attendee_detail"),
    # Registrations
    path("registros/", registration_views.registration_list, name="registration_list"),
    # Posters
    path("eventos/<slug:slug>/poster/", poster_views.event_poster, name="event_poster"),
    path("eventos/<slug:slug>/lineup/", poster_views.lineup_poster, name="lineup_poster"),
]
