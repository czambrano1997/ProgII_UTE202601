from __future__ import annotations

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from events.repositories import room_repository, session_repository


def room_list(request: HttpRequest) -> HttpResponse:
    rooms = room_repository.list_all()
    return render(request, "events/room_list.html", {"rooms": rooms})


def room_detail(request: HttpRequest, pk: int) -> HttpResponse:
    room = room_repository.get_by_id(pk)
    if room is None:
        raise Http404
    sessions = session_repository.list_by_room(pk)
    return render(request, "events/room_detail.html", {"room": room, "sessions": sessions})
