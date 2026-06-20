from __future__ import annotations

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from events.repositories import event_repository


def event_list(request: HttpRequest) -> HttpResponse:
    events = event_repository.list_published()
    return render(request, "events/event_list.html", {"events": events})


def event_detail(request: HttpRequest, slug: str) -> HttpResponse:
    event = event_repository.get_by_slug(slug)
    if event is None:
        raise Http404
    return render(request, "events/event_detail.html", {"event": event})
