from __future__ import annotations

from decimal import Decimal
from typing import Any, Sequence, Union

from django.db import connection

# Public alias matching django's _SQLType without importing the private name.
SQLParam = Union[None, bool, int, float, Decimal, str, bytes]


def fetchall(sql: str, params: Sequence[SQLParam] = ()) -> list[dict[str, Any]]:
    with connection.cursor() as cursor:
        cursor.execute(sql, params)  # type: ignore[arg-type]
        description = cursor.description
        if description is None:
            return []
        columns: list[str] = [col[0] for col in description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
