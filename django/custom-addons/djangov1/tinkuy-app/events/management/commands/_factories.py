# pyright: reportMissingTypeStubs=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUntypedBaseClass=false, reportUnknownArgumentType=false, reportAttributeAccessIssue=false, reportUnknownLambdaType=false, reportPrivateImportUsage=false
"""factory_boy ``DictFactory`` definitions for the demo seeder.

These build **attribute dictionaries** only — they never touch the ORM. The
``seed_demo`` command feeds the dicts into the repository ``get_or_create``
functions, so the single write path (factory -> repository -> Postgres) of
ADR-0006 is preserved. Using ``DictFactory`` (not ``DjangoModelFactory``) is
what keeps the ORM out of the factories.

The leading underscore keeps this module out of Django's command discovery.
"""
from __future__ import annotations

from datetime import timedelta

import factory

from events.models import Level


class RoomDictFactory(factory.DictFactory):
    name = factory.Sequence(lambda n: f"Sala {n + 1}")
    floor = factory.Faker("random_int", min=0, max=6)
    seating_capacity = factory.Faker("random_int", min=20, max=300)
    has_projector = factory.Faker("boolean", chance_of_getting_true=75)
    notes = factory.Faker("sentence", nb_words=6)


class SpeakerDictFactory(factory.DictFactory):
    email = factory.Sequence(lambda n: f"ponente{n + 1}@tinkuy.ec")
    full_name = factory.Faker("name")
    bio = factory.Faker("paragraph", nb_sentences=3)
    twitter_url = factory.LazyAttribute(
        lambda o: f"https://twitter.com/{o.email.split('@')[0]}"
    )
    rating = factory.Faker("pyfloat", min_value=0, max_value=5, right_digits=1)
    # Embedded 1:1 SpeakerProfile fields (upserted by speaker_repository).
    company = factory.Faker("company")
    years_experience = factory.Faker("random_int", min=0, max=30)
    profile_website = factory.Faker("url")


class EventDictFactory(factory.DictFactory):
    slug = factory.Sequence(lambda n: f"evento-{n + 1}")
    name = factory.Faker("catch_phrase")
    summary = factory.Faker("paragraph", nb_sentences=4)
    website = factory.Faker("url")
    start_date = factory.Faker("future_date", end_date="+120d")
    end_date = factory.LazyAttribute(lambda o: o.start_date + timedelta(days=2))
    capacity = factory.Faker("random_int", min=50, max=500)
    ticket_price = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    is_published = True


class SessionDictFactory(factory.DictFactory):
    # FK ids, speakers and the datetime fields are supplied by the command.
    slug = factory.Sequence(lambda n: f"sesion-{n + 1}")
    title = factory.Faker("sentence", nb_words=5)
    abstract = factory.Faker("paragraph", nb_sentences=3)
    level = factory.Faker("random_element", elements=Level.values)
    is_keynote = factory.Faker("boolean", chance_of_getting_true=20)
    max_seats = factory.Faker("random_int", min=20, max=200)


class AttendeeDictFactory(factory.DictFactory):
    email = factory.Sequence(lambda n: f"asistente{n + 1}@tinkuy.ec")
    full_name = factory.Faker("name")
    phone = factory.Faker("numerify", text="09########")
    is_student = factory.Faker("boolean", chance_of_getting_true=60)


class RegistrationDictFactory(factory.DictFactory):
    # attendee_id / session_id are supplied by the command.
    confirmed = factory.Faker("boolean", chance_of_getting_true=70)
    seat_number = factory.Faker("random_int", min=1, max=200)
    amount_paid = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)


ALL_FACTORIES = (
    RoomDictFactory,
    SpeakerDictFactory,
    EventDictFactory,
    SessionDictFactory,
    AttendeeDictFactory,
    RegistrationDictFactory,
)
