from __future__ import annotations

from django.contrib import admin

from events.models import (
    Attendee,
    Event,
    Registration,
    Room,
    Session,
    Speaker,
    SpeakerProfile,
)

__all__ = ["admin"]


class SpeakerProfileInline(admin.StackedInline):  # type: ignore[type-arg]
    model = SpeakerProfile
    extra = 0
    can_delete = False


class RegistrationInline(admin.TabularInline):  # type: ignore[type-arg]
    model = Registration
    extra = 0
    autocomplete_fields = ("attendee",)
    readonly_fields = ("created_at",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ("name", "start_date", "is_published", "capacity")
    list_filter = ("is_published",)
    search_fields = ("name", "summary")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at",)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ("name", "floor", "seating_capacity", "has_projector")
    list_filter = ("has_projector",)
    search_fields = ("name",)


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ("full_name", "email", "rating")
    search_fields = ("full_name", "email")
    inlines = [SpeakerProfileInline]


@admin.register(SpeakerProfile)
class SpeakerProfileAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ("speaker", "company", "years_experience")
    search_fields = ("speaker__full_name", "company")
    autocomplete_fields = ("speaker",)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ("title", "event", "room", "scheduled_at", "is_keynote")
    list_filter = ("level", "is_keynote", "event")
    search_fields = ("title", "abstract")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("speakers",)
    autocomplete_fields = ("event", "room")
    inlines = [RegistrationInline]


@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ("full_name", "email", "is_student", "registered_on")
    list_filter = ("is_student",)
    search_fields = ("full_name", "email")


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ("attendee", "session", "confirmed", "amount_paid")
    list_filter = ("confirmed",)
    autocomplete_fields = ("attendee", "session")
