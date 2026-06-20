from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from events.repositories import registration_repository


def registration_list(request: HttpRequest) -> HttpResponse:
    report = registration_repository.room_utilization()
    return render(request, "events/registration_list.html", {"utilization": report})
