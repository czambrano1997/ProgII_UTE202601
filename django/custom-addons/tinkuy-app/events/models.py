from __future__ import annotations

from decimal import Decimal

from django.db import models


class Level(models.TextChoices):
    BEGINNER = "beginner", "Principiante"
    INTERMEDIATE = "intermediate", "Intermedio"
    ADVANCED = "advanced", "Avanzado"


class Event(models.Model):
    id: int
    name = models.CharField(max_length=200, verbose_name="nombre")
    slug = models.SlugField(unique=True, verbose_name="slug")
    summary = models.TextField(verbose_name="resumen")
    website = models.URLField(blank=True, verbose_name="sitio web")
    start_date = models.DateField(verbose_name="fecha de inicio")
    end_date = models.DateField(verbose_name="fecha de fin")
    is_published = models.BooleanField(default=False, verbose_name="publicado")
    banner = models.ImageField(upload_to="events/banners/", blank=True, verbose_name="banner")
    program_pdf = models.FileField(upload_to="events/programs/", blank=True, verbose_name="programa PDF")
    capacity = models.PositiveIntegerField(verbose_name="capacidad")
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="precio entrada")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="creado en")

    class Meta:
        ordering = ["-start_date"]
        verbose_name = "evento"
        verbose_name_plural = "eventos"

    def __str__(self) -> str:
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=100, verbose_name="nombre")
    floor = models.IntegerField(verbose_name="piso")
    seating_capacity = models.PositiveIntegerField(verbose_name="aforo")
    has_projector = models.BooleanField(default=True, verbose_name="tiene proyector")
    notes = models.TextField(blank=True, verbose_name="notas")

    class Meta:
        ordering = ["floor", "name"]
        verbose_name = "sala"
        verbose_name_plural = "salas"

    def __str__(self) -> str:
        return self.name


class Speaker(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="nombre completo")
    email = models.EmailField(unique=True, verbose_name="correo electrónico")
    bio = models.TextField(verbose_name="biografía")
    photo = models.ImageField(upload_to="speakers/photos/", blank=True, verbose_name="foto")
    twitter_url = models.URLField(blank=True, verbose_name="Twitter")
    rating = models.FloatField(default=0.0, verbose_name="calificación")

    class Meta:
        ordering = ["full_name"]
        verbose_name = "ponente"
        verbose_name_plural = "ponentes"

    def __str__(self) -> str:
        return self.full_name


class SpeakerProfile(models.Model):
    speaker = models.OneToOneField(Speaker, on_delete=models.CASCADE, related_name="profile", verbose_name="ponente")
    company = models.CharField(max_length=200, blank=True, verbose_name="empresa")
    years_experience = models.PositiveSmallIntegerField(default=0, verbose_name="años de experiencia")
    website = models.URLField(blank=True, verbose_name="sitio web")

    class Meta:
        ordering = ["speaker"]
        verbose_name = "perfil de ponente"
        verbose_name_plural = "perfiles de ponente"

    def __str__(self) -> str:
        return f"Perfil de {self.speaker}"


class Session(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="sessions", verbose_name="evento")
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name="sessions", verbose_name="sala")
    speakers: models.ManyToManyField[Speaker, Speaker] = models.ManyToManyField(Speaker, related_name="sessions", verbose_name="ponentes")
    title = models.CharField(max_length=300, verbose_name="título")
    slug = models.SlugField(verbose_name="slug")
    abstract = models.TextField(verbose_name="resumen")
    level = models.CharField(max_length=20, choices=Level.choices, verbose_name="nivel")
    scheduled_at = models.DateTimeField(verbose_name="programado para")
    start_time = models.TimeField(verbose_name="hora de inicio")
    duration = models.DurationField(verbose_name="duración")
    is_keynote = models.BooleanField(default=False, verbose_name="keynote")
    max_seats = models.PositiveIntegerField(verbose_name="plazas máximas")
    recording_url = models.URLField(blank=True, verbose_name="grabación")

    class Meta:
        ordering = ["scheduled_at"]
        unique_together = [("event", "slug")]
        verbose_name = "sesión"
        verbose_name_plural = "sesiones"

    def __str__(self) -> str:
        return self.title


class Attendee(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="nombre completo")
    email = models.EmailField(unique=True, verbose_name="correo electrónico")
    phone = models.CharField(max_length=20, blank=True, verbose_name="teléfono")
    registered_on = models.DateField(auto_now_add=True, verbose_name="fecha de registro")
    is_student = models.BooleanField(default=False, verbose_name="es estudiante")

    class Meta:
        ordering = ["full_name"]
        verbose_name = "asistente"
        verbose_name_plural = "asistentes"

    def __str__(self) -> str:
        return self.full_name


class Registration(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE, related_name="registrations", verbose_name="asistente")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="registrations", verbose_name="sesión")
    confirmed = models.BooleanField(default=False, verbose_name="confirmado")
    seat_number = models.PositiveIntegerField(null=True, blank=True, verbose_name="número de asiento")
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0"), verbose_name="monto pagado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="creado en")

    class Meta:
        ordering = ["-created_at"]
        unique_together = [("attendee", "session")]
        verbose_name = "registro"
        verbose_name_plural = "registros"

    def __str__(self) -> str:
        return f"{self.attendee} → {self.session}"
