---
name: tinkuy-ui-navigation
description: Build Tinkuy's application shell — a persistent navigation drawer plus a minimal app bar (commit 8). Use whenever creating or changing the drawer, the app bar, base.html layout, or the navigation between routes. Replaces the single top nav bar from commit 4 with a left drawer that holds all routing (collapsible mini-rail) and an app bar that carries only the logo and a link home. If you are wiring site-wide navigation or the page shell for Tinkuy, use this.
---

# Tinkuy — App Shell: Drawer Navigation & Minimal App Bar (commit 8)

The site shell is two presentation components: a **persistent navigation drawer**
on the left that owns all routing, and a **minimal app bar** on top that carries
only the logo and a link home. Both are dumb, prop-driven partials surfaced
through typed inclusion tags — same contract as every other Tinkuy component.

**Commit:** `feat: app shell — persistent drawer navigation and minimal app bar`
**Prerequisites:** commit 4 (`tinkuy-views-components`). This **replaces** that
commit's `nav` component (`templates/components/nav.html` + the `nav` tag).

## Why split nav into drawer + app bar

Commit 4 put the logo and every route link in one horizontal bar. As routes grow
that bar gets crowded and the layout has nowhere to put context. The shell pattern
separates concerns:

- **Drawer** = navigation between sections (routing). Always present.
- **App bar** = identity + a single way home. Nothing else.

This is the Material "standard drawer + app bar" layout, kept dependency-free with
Tailwind only (ADR 0004) and Spanish UI copy (ADR 0005).

## App bar (`templates/components/app_bar.html`)

Logo (with the chakana mark, ADR 0005) on the left, a single **Inicio** link on
the right. Nothing else lives here — no route links, no hamburger. Fixed to the top,
offset to the right of the drawer rail.

```html
{# component: app_bar — props: none #}
{% load static %}
<header class="no-print fixed top-0 right-0 left-16 lg:left-64 z-30 h-14
               bg-white border-b border-gray-200 flex items-center justify-between px-4">
  <a href="{% url 'events:event_list' %}"
     class="flex items-center gap-2 font-bold text-lg tracking-tight text-indigo-700">
    {# chakana mark #}
    <svg viewBox="0 0 24 24" class="h-6 w-6" fill="currentColor" fill-rule="evenodd" aria-hidden="true">
      <path d="M10 2H14V6H18V10H22V14H18V18H14V22H10V18H6V14H2V10H6V6H10V2Z M10.5 10.5H13.5V13.5H10.5Z"/>
    </svg>
    Tinkuy
  </a>
  <a href="{% url 'events:event_list' %}"
     class="inline-flex items-center gap-1.5 text-sm text-gray-600 hover:text-indigo-700">
    <svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="1.7"
         stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path d="M3 11.5 12 4l9 7.5"/><path d="M5 10v9a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-9"/><path d="M9.5 20v-6h5v6"/>
    </svg>
    Inicio
  </a>
</header>
```

The app bar's left edge tracks the drawer's **rail** width (`left-16 lg:left-64`),
not its hover-expanded width — the drawer overlays on hover, it does not reflow the
page.

## Drawer (`templates/components/drawer.html`)

A **persistent** drawer fixed full-height on the left. It collapses to an
icons-only **mini-rail** (`w-16`) on small screens and is fully expanded (`w-64`)
from `lg` up. On small screens it expands two ways:

- **Hover** — pure CSS via Tailwind's `group` / `group-hover` and a width transition.
- **Click** — a toggle button pins it open; ~10 lines of vanilla JS flip an
  `is-open` class and `aria-expanded`. A tiny scoped `<style>` block (the only CSS
  outside Tailwind in this project) expresses the pinned width and label visibility
  so the click state never depends on exotic generated utilities.

Every link is icon + label: the icon is always visible (so the rail is usable
collapsed), the label fades in when the drawer is expanded. Active state is computed
from the current route name passed in as the `current` prop.

```html
{# component: drawer — props: current:str="" (active route url_name) #}
<aside id="app-drawer"
       class="no-print group fixed inset-y-0 left-0 z-40 flex flex-col overflow-x-hidden
              w-16 hover:w-64 lg:w-64 bg-indigo-700 text-white shadow-lg
              transition-[width] duration-200 ease-in-out">

  {# brand row — chakana glyph always visible, wordmark on expand #}
  <div class="flex items-center h-14 px-3 shrink-0">
    <span class="grid place-items-center h-10 w-10 shrink-0">
      <svg viewBox="0 0 24 24" class="h-6 w-6" fill="currentColor" fill-rule="evenodd" aria-hidden="true">
        <path d="M10 2H14V6H18V10H22V14H18V18H14V22H10V18H6V14H2V10H6V6H10V2Z M10.5 10.5H13.5V13.5H10.5Z"/>
      </svg>
    </span>
    <span class="drawer-label ml-2 font-semibold tracking-tight whitespace-nowrap
                 opacity-0 transition-opacity duration-200 group-hover:opacity-100 lg:opacity-100">Tinkuy</span>
  </div>

  <nav class="flex-1 px-2 py-2 space-y-1" aria-label="Navegación principal">
    {# one entry per section. Pattern: icon (always) + label (fades in) + active state #}
    <a href="{% url 'events:event_list' %}"
       class="flex items-center h-11 rounded-lg px-3
              {% if current == 'event_list' or current == 'event_detail' or current == 'session_list' or current == 'session_detail' or current == 'event_poster' or current == 'lineup_poster' %}bg-indigo-900 text-white{% else %}text-indigo-100 hover:bg-indigo-600{% endif %}">
      <svg viewBox="0 0 24 24" class="h-6 w-6 shrink-0" fill="none" stroke="currentColor" stroke-width="1.7"
           stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <rect x="3" y="4.5" width="18" height="16" rx="2"/><path d="M3 9h18M8 3v3M16 3v3"/>
      </svg>
      <span class="drawer-label ml-3 text-sm whitespace-nowrap opacity-0 transition-opacity duration-200 group-hover:opacity-100 lg:opacity-100">Eventos</span>
    </a>

    <a href="{% url 'events:speaker_list' %}"
       class="flex items-center h-11 rounded-lg px-3
              {% if current == 'speaker_list' or current == 'speaker_detail' %}bg-indigo-900 text-white{% else %}text-indigo-100 hover:bg-indigo-600{% endif %}">
      <svg viewBox="0 0 24 24" class="h-6 w-6 shrink-0" fill="none" stroke="currentColor" stroke-width="1.7"
           stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3M8.5 21h7"/>
      </svg>
      <span class="drawer-label ml-3 text-sm whitespace-nowrap opacity-0 transition-opacity duration-200 group-hover:opacity-100 lg:opacity-100">Ponentes</span>
    </a>

    <a href="{% url 'events:room_list' %}"
       class="flex items-center h-11 rounded-lg px-3
              {% if current == 'room_list' or current == 'room_detail' %}bg-indigo-900 text-white{% else %}text-indigo-100 hover:bg-indigo-600{% endif %}">
      <svg viewBox="0 0 24 24" class="h-6 w-6 shrink-0" fill="none" stroke="currentColor" stroke-width="1.7"
           stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <rect x="4" y="3" width="16" height="18" rx="1.5"/><path d="M8 7h.01M12 7h.01M16 7h.01M8 11h.01M12 11h.01M16 11h.01M10 21v-4h4v4"/>
      </svg>
      <span class="drawer-label ml-3 text-sm whitespace-nowrap opacity-0 transition-opacity duration-200 group-hover:opacity-100 lg:opacity-100">Salas</span>
    </a>

    <a href="{% url 'events:attendee_list' %}"
       class="flex items-center h-11 rounded-lg px-3
              {% if current == 'attendee_list' or current == 'attendee_detail' %}bg-indigo-900 text-white{% else %}text-indigo-100 hover:bg-indigo-600{% endif %}">
      <svg viewBox="0 0 24 24" class="h-6 w-6 shrink-0" fill="none" stroke="currentColor" stroke-width="1.7"
           stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <circle cx="9" cy="8" r="3.2"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0M16 5.6a3 3 0 0 1 0 5.8M17.5 14.2c2.3.6 4 2.6 4 5.8"/>
      </svg>
      <span class="drawer-label ml-3 text-sm whitespace-nowrap opacity-0 transition-opacity duration-200 group-hover:opacity-100 lg:opacity-100">Asistentes</span>
    </a>

    <a href="{% url 'events:registration_list' %}"
       class="flex items-center h-11 rounded-lg px-3
              {% if current == 'registration_list' %}bg-indigo-900 text-white{% else %}text-indigo-100 hover:bg-indigo-600{% endif %}">
      <svg viewBox="0 0 24 24" class="h-6 w-6 shrink-0" fill="none" stroke="currentColor" stroke-width="1.7"
           stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M3 8a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2 2 2 0 0 0 0 4 2 2 0 0 1-2 2H5a2 2 0 0 1-2-2 2 2 0 0 0 0-4Z"/><path d="M9 6.5v11" stroke-dasharray="2 2"/>
      </svg>
      <span class="drawer-label ml-3 text-sm whitespace-nowrap opacity-0 transition-opacity duration-200 group-hover:opacity-100 lg:opacity-100">Registros</span>
    </a>
  </nav>

  {# pin toggle — the only control; honors "app bar = logo + Inicio only" #}
  <button type="button" data-drawer-toggle aria-controls="app-drawer" aria-expanded="false"
          class="flex items-center h-12 m-2 rounded-lg px-3 text-indigo-100 hover:bg-indigo-600">
    <svg viewBox="0 0 24 24" class="h-6 w-6 shrink-0" fill="none" stroke="currentColor" stroke-width="1.7"
         stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path d="M4 7h16M4 12h16M4 17h16"/>
    </svg>
    <span class="drawer-label ml-3 text-sm whitespace-nowrap opacity-0 transition-opacity duration-200 group-hover:opacity-100 lg:opacity-100">Fijar menú</span>
  </button>

  {# click-to-pin: width + label visibility for the pinned state only #}
  <style>
    #app-drawer.is-open { width: 16rem; }
    #app-drawer.is-open .drawer-label { opacity: 1; }
  </style>
  <script>
    (function () {
      var d = document.getElementById("app-drawer");
      var btn = d && d.querySelector("[data-drawer-toggle]");
      if (!d || !btn) return;
      btn.addEventListener("click", function () {
        var open = d.classList.toggle("is-open");
        btn.setAttribute("aria-expanded", open ? "true" : "false");
      });
    })();
  </script>
</aside>
```

## Inclusion tags (`events/templatetags/components.py`)

Typed, like every other component. The drawer needs the current route name, so it
takes context (the `request` context processor is enabled in settings). **Remove**
the old `nav` tag.

```python
@register.inclusion_tag("components/app_bar.html")
def app_bar() -> dict[str, str]:
    return {}


@register.inclusion_tag("components/drawer.html", takes_context=True)
def drawer(context: template.Context) -> dict[str, str]:
    request = context.get("request")
    match = getattr(request, "resolver_match", None)
    current = str(getattr(match, "url_name", "") or "")
    return {"current": current}
```

## base.html integration

Render the drawer and app bar, then inset `<main>` by the rail width and the app
bar height. Add a `{% block extra_head %}` — posters (commit 6) already define it
for their print stylesheet, so without it that CSS is silently dropped.

```html
{% load static %}{% load components %}<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{% block title %}Tinkuy{% endblock %}</title>
  <link rel="stylesheet" href="{% static 'css/tailwind.css' %}" />
  {% block extra_head %}{% endblock %}
</head>
<body class="bg-gray-50 min-h-screen">
  {% drawer %}
  {% app_bar %}
  <main class="ml-16 lg:ml-64 pt-14">
    <div class="max-w-6xl mx-auto px-4 py-8">
      {% block content %}{% endblock %}
    </div>
  </main>
</body>
</html>
```

Because posters extend `base.html`, neutralize the shell in their print stylesheet
(`templates/posters/poster_base.html`) so posters print edge-to-edge:

```css
@media print {
  header, aside { display: none; }
  main { margin: 0 !important; padding-top: 0 !important; }
}
```

## Component conventions (unchanged from commit 4)

- One component = one partial in `components/` + one typed inclusion tag. The drawer
  and app bar follow this exactly; the drawer's `<style>`/`<script>` stay **inside**
  its partial so the component is self-contained.
- Presentation only: explicit props, no queries, no business logic. The active route
  is derived from `request` in the tag and passed down as a plain string.
- Keep the prop-contract comment accurate — it is the component's interface.
- Migration target (ADR 0003): `app_bar`/`drawer` become `<c-app-bar>` / `<c-drawer>`
  in `django-cotton` / `django-components` without moving files.

## Build (Tailwind)

The shell adds new utilities (rail widths, `group-hover`, `transition-[width]`,
offsets). Rebuild the stylesheet:

```bash
make tailwind        # uv run tailwindcss -i static/src/input.css -o static/css/tailwind.css
```

> **Tailwind v4 note:** `static/src/input.css` must use `@import "tailwindcss";`,
> not the v3 `@tailwind base/components/utilities` directives. Under v4 the old
> directives load no theme, so every spacing/color/breakpoint utility (`w-16`,
> `bg-indigo-700`, `lg:*`, …) is silently dropped and the shell renders unstyled.

## Definition of done

- The old single nav bar is gone: `nav.html` and the `nav` tag are removed and no
  template references `{% nav %}`.
- `app_bar` renders only the logo and an **Inicio** link; `drawer` holds every route.
- The drawer is a persistent mini-rail: icons-only at `w-16`, expands to `w-64` on
  hover and on `lg`, and pins open on click (`aria-expanded` reflects state).
- Active route is highlighted from the current `url_name`.
- `base.html` insets `<main>` for the shell and declares `{% block extra_head %}`;
  posters still print edge-to-edge.
- Tailwind is rebuilt; every page renders (existing view tests stay green).
- `uv run pyright` is clean under strict mode.

## References

- `docs/adr/0003-presentation-fbv-and-components.md` (inclusion-tag components),
  `docs/adr/0004-styling-tailwind.md` (Tailwind-only), `docs/adr/0005-naming-tinkuy-kichwa.md` (chakana, Spanish copy).
- Supersedes the `nav` component from `tinkuy-views-components` (commit 4).
