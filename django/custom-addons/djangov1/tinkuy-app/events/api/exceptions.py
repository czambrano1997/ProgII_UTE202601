# pyright: reportMissingTypeStubs=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportUnknownParameterType=false, reportMissingParameterType=false
"""Custom DRF exception handler.

Database constraint violations bubble up from the repository write functions as
``IntegrityError`` (and its subclass ``ProtectedError`` for protected FKs). The
default DRF handler turns those into a 500; we map them to a clean 409 Conflict
so duplicate natural keys (slug/email/unique_together) and protected deletes are
reported as client errors instead of crashes.
"""
from __future__ import annotations

from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if response is not None:
        return response
    if isinstance(exc, IntegrityError):
        return Response({"detail": str(exc)}, status=status.HTTP_409_CONFLICT)
    return None
