from __future__ import annotations

from typing import Any, cast

from events.models import SiteConfiguration


def get_value(key: str, default: Any = None) -> Any:
    config = SiteConfiguration.objects.filter(key=key).first()
    return config.value if config is not None else default


def get_by_prefix(prefix: str) -> list[Any]:
    configs = SiteConfiguration.objects.filter(key__startswith=prefix)
    values: list[Any] = [config.value for config in configs]

    def order_of(value: Any) -> int:
        if isinstance(value, dict):
            order = cast("dict[str, Any]", value).get("order", 0)
            return order if isinstance(order, int) else 0
        return 0

    values.sort(key=order_of)
    return values
