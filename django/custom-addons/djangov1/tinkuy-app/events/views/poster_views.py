from __future__ import annotations

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from events.repositories import event_repository, session_repository


def event_poster(request: HttpRequest, slug: str) -> HttpResponse:
    event = event_repository.get_by_slug(slug)
    if event is None:
        raise Http404
    sessions = session_repository.list_by_event(event.id)
    keynotes = session_repository.list_keynotes(event.id)
    return render(
        request,
        "posters/event_poster.html",
        {"event": event, "sessions": sessions, "keynotes": keynotes},
    )


def lineup_poster(request: HttpRequest, slug: str) -> HttpResponse:
    event = event_repository.get_by_slug(slug)
    if event is None:
        raise Http404
    sessions = session_repository.list_keynotes(event.id)
    return render(
        request,
        "posters/lineup_poster.html",
        {"event": event, "sessions": sessions},
    )
