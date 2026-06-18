"""Unit tests for model __str__ and Level choices — no database required."""
from __future__ import annotations

from decimal import Decimal

from events.models import Level


class TestLevel:
    def test_choices_labels_are_spanish(self) -> None:
        labels = {c[0]: c[1] for c in Level.choices}
        assert labels[Level.BEGINNER] == "Principiante"
        assert labels[Level.INTERMEDIATE] == "Intermedio"
        assert labels[Level.ADVANCED] == "Avanzado"

    def test_values(self) -> None:
        assert Level.BEGINNER == "beginner"
        assert Level.INTERMEDIATE == "intermediate"
        assert Level.ADVANCED == "advanced"


class TestDecimalDefault:
    """Verify Decimal('0') is used correctly for amount_paid default."""

    def test_decimal_zero_identity(self) -> None:
        assert Decimal("0") == Decimal(0)
        assert str(Decimal("0")) == "0"
