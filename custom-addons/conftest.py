"""
conftest.py
===========
Stub del runtime de Odoo para ejecutar los tests unitarios con pytest puro,
sin necesitar el servidor Odoo instalado ni una base de datos.

Cómo funciona
-------------
pytest importa este archivo ANTES de cualquier módulo de test.
Aquí registramos módulos falsos en sys.modules para que los imports
del tipo `from odoo import models, fields` no fallen.

Las excepciones (UserError, ValidationError) son clases REALES que heredan
de Exception, para que assertRaises() funcione correctamente en los tests.

Colocar este archivo en: custom-addons/conftest.py
"""

import sys
from types import ModuleType
from unittest.mock import MagicMock


# ---------------------------------------------------------------------------
# 1. Excepciones reales (no mocks) — imprescindible para assertRaises()
# ---------------------------------------------------------------------------

class UserError(Exception):
    """Stub de odoo.exceptions.UserError."""
    pass


class ValidationError(UserError):
    """Stub de odoo.exceptions.ValidationError."""
    pass


class AccessError(UserError):
    """Stub de odoo.exceptions.AccessError."""
    pass


# ---------------------------------------------------------------------------
# 2. Módulo odoo.exceptions como módulo real con las clases anteriores
# ---------------------------------------------------------------------------

_exceptions_mod = ModuleType("odoo.exceptions")
_exceptions_mod.UserError = UserError
_exceptions_mod.ValidationError = ValidationError
_exceptions_mod.AccessError = AccessError

# ---------------------------------------------------------------------------
# 3. Resto de submódulos odoo → MagicMock (no se usan en tests unitarios)
# ---------------------------------------------------------------------------

_odoo_mod = MagicMock(name="odoo")
_odoo_mod.exceptions = _exceptions_mod

# Exponer las excepciones también desde el mock raíz para:
#   from odoo.exceptions import UserError  (acceso directo)
_odoo_mod.exceptions.UserError = UserError
_odoo_mod.exceptions.ValidationError = ValidationError
_odoo_mod.exceptions.AccessError = AccessError

# ---------------------------------------------------------------------------
# 4. Registrar en sys.modules (setdefault: no pisa si ya existe)
# ---------------------------------------------------------------------------

_STUBS: dict[str, object] = {
    "odoo":                 _odoo_mod,
    "odoo.exceptions":      _exceptions_mod,
    "odoo.models":          MagicMock(name="odoo.models"),
    "odoo.fields":          MagicMock(name="odoo.fields"),
    "odoo.api":             MagicMock(name="odoo.api"),
    "odoo.tests":           MagicMock(name="odoo.tests"),
    "odoo.tests.common":    MagicMock(name="odoo.tests.common"),
    "odoo.tools":           MagicMock(name="odoo.tools"),
    "odoo.tools.misc":      MagicMock(name="odoo.tools.misc"),
}

for _name, _stub in _STUBS.items():
    sys.modules.setdefault(_name, _stub)
