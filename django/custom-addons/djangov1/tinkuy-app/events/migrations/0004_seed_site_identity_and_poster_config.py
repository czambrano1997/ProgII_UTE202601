from __future__ import annotations

from django.db import migrations

SITE_CONFIGURATION = {
    "site.currency_symbol": "$",
    "site.tagline": "Tinkuy · «encuentro de mundos»",
    "site.footer_text": "Tinkuy — plataforma de eventos universitarios",
    "site.cultural_note": (
        '<strong class="text-white">Tinkuy</strong> — vocablo kichwa que significa '
        "<em>«el encuentro de dos mundos o fuerzas»</em>."
    ),
    "site.domain": "tinkuy.ec",
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
        ("events", "0003_seed_site_configuration"),
    ]

    operations = [
        migrations.RunPython(seed_site_configuration, unseed_site_configuration),
    ]
