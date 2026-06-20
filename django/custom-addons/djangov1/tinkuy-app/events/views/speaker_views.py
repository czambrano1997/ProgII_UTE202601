from __future__ import annotations

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from events.repositories import speaker_repository


def speaker_list(request: HttpRequest) -> HttpResponse:
    speakers = speaker_repository.list_all()
    return render(request, "events/speaker_list.html", {"speakers": speakers})


def speaker_detail(request: HttpRequest, pk: int) -> HttpResponse:
    speaker = speaker_repository.get_by_id(pk)
    if speaker is None:
        raise Http404
    profile = speaker_repository.get_profile(pk)
    return render(request, "events/speaker_detail.html", {"speaker": speaker, "profile": profile})
