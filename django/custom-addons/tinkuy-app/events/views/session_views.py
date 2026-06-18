from __future__ import annotations

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from events.repositories import session_repository


def session_list(request: HttpRequest, event_id: int) -> HttpResponse:
    sessions = session_repository.list_by_event(event_id)
    return render(request, "events/session_list.html", {"sessions": sessions, "event_id": event_id})


def session_detail(request: HttpRequest, event_id: int, slug: str) -> HttpResponse:
    session = session_repository.get_by_slug(event_id, slug)
    if session is None:
        raise Http404
    return render(request, "events/session_detail.html", {"session": session})
