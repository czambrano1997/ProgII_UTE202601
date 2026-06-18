from __future__ import annotations

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from events.repositories import attendee_repository


def attendee_list(request: HttpRequest) -> HttpResponse:
    attendees = attendee_repository.list_students()
    return render(request, "events/attendee_list.html", {"attendees": attendees})


def attendee_detail(request: HttpRequest, pk: int) -> HttpResponse:
    attendee = attendee_repository.get_by_id(pk)
    if attendee is None:
        raise Http404
    registrations = attendee_repository.list_registrations(pk)
    return render(request, "events/attendee_detail.html", {"attendee": attendee, "registrations": registrations})
