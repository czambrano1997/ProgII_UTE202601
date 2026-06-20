from __future__ import annotations

from django.db import migrations

NAV_ICON_EVENTS = (
    '<svg viewBox="0 0 24 24" class="h-6 w-6 shrink-0" fill="none" stroke="currentColor" '
    'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<rect x="3" y="4.5" width="18" height="16" rx="2"/><path d="M3 9h18M8 3v3M16 3v3"/></svg>'
)
NAV_ICON_SPEAKERS = (
    '<svg viewBox="0 0 24 24" class="h-6 w-6 shrink-0" fill="none" stroke="currentColor" '
    'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3M8.5 21h7"/></svg>'
)
NAV_ICON_ROOMS = (
    '<svg viewBox="0 0 24 24" class="h-6 w-6 shrink-0" fill="none" stroke="currentColor" '
    'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<rect x="4" y="3" width="16" height="18" rx="1.5"/>'
    '<path d="M8 7h.01M12 7h.01M16 7h.01M8 11h.01M12 11h.01M16 11h.01M10 21v-4h4v4"/></svg>'
)
NAV_ICON_ATTENDEES = (
    '<svg viewBox="0 0 24 24" class="h-6 w-6 shrink-0" fill="none" stroke="currentColor" '
    'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<circle cx="9" cy="8" r="3.2"/>'
    '<path d="M2.5 20a6.5 6.5 0 0 1 13 0M16 5.6a3 3 0 0 1 0 5.8M17.5 14.2c2.3.6 4 2.6 4 5.8"/></svg>'
)
NAV_ICON_REGISTRATIONS = (
    '<svg viewBox="0 0 24 24" class="h-6 w-6 shrink-0" fill="none" stroke="currentColor" '
    'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M3 8a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2 2 2 0 0 0 0 4 2 2 0 0 1-2 2H5a2 2 0 0 1-2-2 2 2 0 0 0 0-4Z"/>'
    '<path d="M9 6.5v11" stroke-dasharray="2 2"/></svg>'
)
CHAKANA_ICON = (
    '<svg viewBox="0 0 24 24" class="h-6 w-6" fill="currentColor" fill-rule="evenodd" aria-hidden="true">'
    '<path d="M10 2H14V6H18V10H22V14H18V18H14V22H10V18H6V14H2V10H6V6H10V2Z M10.5 10.5H13.5V13.5H10.5Z"/></svg>'
)

SITE_CONFIGURATION = {
    "nav.events": {
        "order": 1,
        "label": "Eventos",
        "url": "events:event_list",
        "active_urls": [
            "event_list",
            "event_detail",
            "session_list",
            "session_detail",
            "event_poster",
            "lineup_poster",
        ],
        "icon": NAV_ICON_EVENTS,
    },
    "nav.speakers": {
        "order": 2,
        "label": "Ponentes",
        "url": "events:speaker_list",
        "active_urls": ["speaker_list", "speaker_detail"],
        "icon": NAV_ICON_SPEAKERS,
    },
    "nav.rooms": {
        "order": 3,
        "label": "Salas",
        "url": "events:room_list",
        "active_urls": ["room_list", "room_detail"],
        "icon": NAV_ICON_ROOMS,
    },
    "nav.attendees": {
        "order": 4,
        "label": "Asistentes",
        "url": "events:attendee_list",
        "active_urls": ["attendee_list", "attendee_detail"],
        "icon": NAV_ICON_ATTENDEES,
    },
    "nav.registrations": {
        "order": 5,
        "label": "Registros",
        "url": "events:registration_list",
        "active_urls": ["registration_list"],
        "icon": NAV_ICON_REGISTRATIONS,
    },
    "site.brand_name": "Tinkuy",
    "site.home_url": "events:event_list",
    "site.brand_icon": CHAKANA_ICON,
}


def seed_site_configuration(apps, schema_editor):
    SiteConfiguration = apps.get_model("events", "SiteConfiguration")
    for key, value in SITE_CONFIGURATION.items():
        SiteConfiguration.objects.update_or_create(key=key, defaults={"value": value})


def unseed_site_configuration(apps, schema_editor):
    SiteConfiguration = apps.get_model("events", "SiteConfiguration")
    SiteConfiguration.objects.filter(key__in=SITE_CONFIGURATION.keys()).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0002_siteconfiguration"),
    ]

    operations = [
        migrations.RunPython(seed_site_configuration, unseed_site_configuration),
    ]
