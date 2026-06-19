from __future__ import annotations

from django import template

register = template.Library()


@register.inclusion_tag("components/app_bar.html")
def app_bar() -> dict[str, str]:
    return {}


@register.inclusion_tag("components/drawer.html", takes_context=True)
def drawer(context: template.Context) -> dict[str, str]:
    request = context.get("request")
    match = getattr(request, "resolver_match", None)
    current = str(getattr(match, "url_name", "") or "")
    return {"current": current}


@register.inclusion_tag("components/page_header.html")
def page_header(title: str, subtitle: str = "") -> dict[str, str]:
    return {"title": title, "subtitle": subtitle}


@register.inclusion_tag("components/card.html")
def card(title: str, subtitle: str = "", href: str = "") -> dict[str, str]:
    return {"title": title, "subtitle": subtitle, "href": href}


@register.inclusion_tag("components/badge.html")
def badge(label: str, color: str = "blue") -> dict[str, str]:
    return {"label": label, "color": color}


@register.inclusion_tag("components/stat.html")
def stat(label: str, value: str) -> dict[str, str]:
    return {"label": label, "value": value}


@register.inclusion_tag("components/empty_state.html")
def empty_state(message: str) -> dict[str, str]:
    return {"message": message}
