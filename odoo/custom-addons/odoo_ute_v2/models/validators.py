import re

from odoo.exceptions import ValidationError


PERSONA_RE = re.compile(
    r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+"
    r"(?:[ '\-][A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+)*$"
)

TEXTO_RE = re.compile(
    r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9 .,'()/#&+\-]+$"
)

LETRA_RE = re.compile(
    r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]"
)

EMAIL_RE = re.compile(
    r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
)

TELEFONO_RE = re.compile(
    r"^0\d{9}$"
)

CEDULA_RE = re.compile(
    r"^\d{10}$"
)

CODIGO_RE = re.compile(
    r"^(?=.*[A-Za-z])[A-Za-z0-9-]{2,15}$"
)

PERIODO_RE = re.compile(
    r"^\d{4}-(?:1|2)$"
)


def limpiar(valor):
    """Elimina espacios al inicio y al final."""
    return (valor or "").strip()


def validar_persona(valor, etiqueta):
    """
    Valida nombres y apellidos.

    Permite:
    - Letras
    - Espacios
    - Apóstrofos
    - Guiones

    No permite números.
    """
    valor = limpiar(valor)

    if not 2 <= len(valor) <= 80:
        raise ValidationError(
            f"{etiqueta} debe tener entre 2 y 80 caracteres."
        )

    if not PERSONA_RE.fullmatch(valor):
        raise ValidationError(
            f"{etiqueta} solo puede contener letras, espacios, "
            "apóstrofos y guiones."
        )


def validar_texto(valor, etiqueta, maximo=100):
    """
    Valida nombres de materias, carreras, aulas y edificios.

    Puede contener números, pero debe tener al menos una letra.
    Por ejemplo: Aula 301 o Matemática 2 son válidos.
    """
    valor = limpiar(valor)

    if not 2 <= len(valor) <= maximo:
        raise ValidationError(
            f"{etiqueta} debe tener entre 2 y {maximo} caracteres."
        )

    if not TEXTO_RE.fullmatch(valor):
        raise ValidationError(
            f"{etiqueta} contiene caracteres no permitidos."
        )

    if not LETRA_RE.search(valor):
        raise ValidationError(
            f"{etiqueta} debe contener al menos una letra. "
            "No puede estar formado únicamente por números."
        )


def validar_email(valor):
    """Valida un correo electrónico básico."""
    valor = limpiar(valor)

    if not EMAIL_RE.fullmatch(valor):
        raise ValidationError(
            "Ingrese un correo electrónico válido."
        )


def validar_telefono(valor):
    """
    Valida teléfono ecuatoriano usado por el proyecto.

    Debe contener exactamente 10 dígitos y comenzar con cero.
    """
    valor = limpiar(valor)

    if not TELEFONO_RE.fullmatch(valor):
        raise ValidationError(
            "El teléfono debe contener exactamente 10 dígitos "
            "y comenzar con 0."
        )


def validar_identificacion(valor):
    """
    Valida una cédula ecuatoriana de persona natural.

    Reglas:
    - Exactamente 10 dígitos.
    - Código provincial 01-24 o código exterior 30.
    - Tercer dígito entre 0 y 5.
    - Dígito verificador válido mediante módulo 10.
    """
    cedula = limpiar(valor)

    if not CEDULA_RE.fullmatch(cedula):
        raise ValidationError(
            "La cédula ecuatoriana debe contener exactamente "
            "10 dígitos numéricos."
        )

    codigo_provincia = int(cedula[:2])

    provincia_valida = (
        1 <= codigo_provincia <= 24
        or codigo_provincia == 30
    )

    if not provincia_valida:
        raise ValidationError(
            "Los dos primeros dígitos deben corresponder "
            "a una provincia del Ecuador entre 01 y 24, "
            "o utilizar el código 30 para registros del exterior."
        )

    tercer_digito = int(cedula[2])

    if tercer_digito > 5:
        raise ValidationError(
            "La identificación no corresponde a una cédula "
            "ecuatoriana de persona natural."
        )

    coeficientes = (
        2,
        1,
        2,
        1,
        2,
        1,
        2,
        1,
        2,
    )

    suma = 0

    for digito_texto, coeficiente in zip(
        cedula[:9],
        coeficientes,
    ):
        producto = int(digito_texto) * coeficiente

        if producto >= 10:
            producto -= 9

        suma += producto

    digito_verificador_calculado = (
        10 - (suma % 10)
    ) % 10

    digito_verificador_ingresado = int(cedula[9])

    if (
        digito_verificador_calculado
        != digito_verificador_ingresado
    ):
        raise ValidationError(
            "La cédula ecuatoriana no es válida: "
            "el dígito verificador es incorrecto."
        )


def validar_codigo(valor):
    """Valida códigos de carrera."""
    valor = limpiar(valor)

    if not CODIGO_RE.fullmatch(valor):
        raise ValidationError(
            "El código debe tener entre 2 y 15 caracteres, "
            "contener al menos una letra y usar únicamente "
            "letras, números o guiones."
        )


def validar_periodo(valor):
    """Valida nombres de periodo como 2025-1 o 2025-2."""
    valor = limpiar(valor)

    if not PERIODO_RE.fullmatch(valor):
        raise ValidationError(
            "El periodo debe tener el formato AAAA-1 o AAAA-2. "
            "Ejemplo: 2025-2."
        )
