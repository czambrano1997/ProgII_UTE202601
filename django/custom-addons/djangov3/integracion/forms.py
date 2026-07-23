import re

from django import forms

from .config import obtener_config


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


def validar_texto_con_letra(
    valor,
    etiqueta,
    maximo=100,
):
    """
    Valida textos que pueden tener números,
    pero deben contener al menos una letra.
    """
    valor = (valor or "").strip()

    if not 2 <= len(valor) <= maximo:
        raise forms.ValidationError(
            f"{etiqueta} debe tener entre "
            f"2 y {maximo} caracteres."
        )

    if not TEXTO_RE.fullmatch(valor):
        raise forms.ValidationError(
            f"{etiqueta} contiene caracteres no permitidos."
        )

    if not LETRA_RE.search(valor):
        raise forms.ValidationError(
            f"{etiqueta} debe contener al menos una letra. "
            "No puede estar formado únicamente por números."
        )

    return valor


def validar_cedula_ecuatoriana(valor):
    """
    Valida una cédula ecuatoriana de persona natural.

    Reglas:
    - Exactamente 10 dígitos.
    - Código provincial 01-24 o exterior 30.
    - Tercer dígito entre 0 y 5.
    - Dígito verificador válido.
    """
    cedula = (valor or "").strip()

    if not CEDULA_RE.fullmatch(cedula):
        raise forms.ValidationError(
            "La cédula ecuatoriana debe contener exactamente "
            "10 dígitos numéricos."
        )

    codigo_provincia = int(cedula[:2])

    provincia_valida = (
        1 <= codigo_provincia <= 24
        or codigo_provincia == 30
    )

    if not provincia_valida:
        raise forms.ValidationError(
            "Los dos primeros dígitos deben corresponder "
            "a una provincia del Ecuador entre 01 y 24, "
            "o utilizar el código 30 para registros del exterior."
        )

    tercer_digito = int(cedula[2])

    if tercer_digito > 5:
        raise forms.ValidationError(
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

    digito_verificador_ingresado = int(
        cedula[9]
    )

    if (
        digito_verificador_calculado
        != digito_verificador_ingresado
    ):
        raise forms.ValidationError(
            "La cédula ecuatoriana no es válida: "
            "el dígito verificador es incorrecto."
        )

    return cedula


class RegistroOdooForm(forms.Form):
    """
    Formulario genérico utilizado por los cinco modelos.
    """

    def __init__(
        self,
        *args,
        modelo,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.modelo = modelo

        config = obtener_config(modelo)

        if config is None:
            raise ValueError(
                f"Modelo no soportado: {modelo}"
            )

        for campo in config["campos"]:
            comunes = {
                "label": campo["label"],
                "required": campo.get(
                    "required",
                    False,
                ),
                "initial": campo.get("initial"),
            }

            tipo = campo["type"]

            if tipo == "email":
                campo_formulario = forms.EmailField(
                    max_length=campo.get(
                        "max_length",
                        120,
                    ),
                    **comunes,
                )

            elif tipo == "date":
                campo_formulario = forms.DateField(
                    widget=forms.DateInput(
                        attrs={
                            "type": "date",
                        }
                    ),
                    **comunes,
                )

            elif tipo == "integer":
                campo_formulario = forms.IntegerField(
                    min_value=campo.get(
                        "min_value",
                    ),
                    max_value=campo.get(
                        "max_value",
                    ),
                    **comunes,
                )

            elif tipo == "boolean":
                campo_formulario = forms.BooleanField(
                    **comunes,
                )

            elif tipo == "choice":
                campo_formulario = forms.ChoiceField(
                    choices=campo["choices"],
                    **comunes,
                )

            else:
                campo_formulario = forms.CharField(
                    min_length=campo.get(
                        "min_length",
                    ),
                    max_length=campo.get(
                        "max_length",
                        255,
                    ),
                    **comunes,
                )

            campo_formulario.widget.attrs.setdefault(
                "class",
                "form-control",
            )

            if tipo == "boolean":
                campo_formulario.widget.attrs["class"] = (
                    "form-check-input"
                )

            for atributo, valor in campo.get(
                "widget_attrs",
                {},
            ).items():
                campo_formulario.widget.attrs[
                    atributo
                ] = valor

            self.fields[
                campo["name"]
            ] = campo_formulario

    def clean(self):
        datos = super().clean()

        # Limpiar espacios de todos los textos.
        for nombre, valor in tuple(
            datos.items()
        ):
            if isinstance(valor, str):
                datos[nombre] = valor.strip()

        # ----------------------------------------------------
        # MATERIAS
        # ----------------------------------------------------
        if self.modelo == "signature":
            nombre = datos.get("name")

            if nombre:
                try:
                    datos["name"] = (
                        validar_texto_con_letra(
                            nombre,
                            "El nombre de la materia",
                        )
                    )
                except forms.ValidationError as error:
                    self.add_error(
                        "name",
                        error,
                    )

        # ----------------------------------------------------
        # DOCENTES
        # ----------------------------------------------------
        elif self.modelo == "usuarios":
            for campo, etiqueta in (
                (
                    "name",
                    "Los nombres",
                ),
                (
                    "last_name",
                    "Los apellidos",
                ),
            ):
                valor = datos.get(campo)

                if (
                    valor
                    and not PERSONA_RE.fullmatch(valor)
                ):
                    self.add_error(
                        campo,
                        (
                            f"{etiqueta} solo puede contener "
                            "letras, espacios, apóstrofos "
                            "y guiones."
                        ),
                    )

            telefono = datos.get("phone")

            if (
                telefono
                and not TELEFONO_RE.fullmatch(
                    telefono
                )
            ):
                self.add_error(
                    "phone",
                    (
                        "El teléfono debe contener "
                        "exactamente 10 dígitos "
                        "y comenzar con 0."
                    ),
                )

            cedula = datos.get("vat")

            if cedula:
                try:
                    datos["vat"] = (
                        validar_cedula_ecuatoriana(
                            cedula
                        )
                    )
                except forms.ValidationError as error:
                    self.add_error(
                        "vat",
                        error,
                    )

            correo = datos.get("email")

            if correo:
                datos["email"] = correo.lower()

        # ----------------------------------------------------
        # CARRERAS
        # ----------------------------------------------------
        elif self.modelo == "carrera":
            nombre = datos.get("name")

            if nombre:
                try:
                    datos["name"] = (
                        validar_texto_con_letra(
                            nombre,
                            "El nombre de la carrera",
                        )
                    )
                except forms.ValidationError as error:
                    self.add_error(
                        "name",
                        error,
                    )

            codigo = datos.get("codigo")

            if codigo:
                codigo = codigo.upper()
                datos["codigo"] = codigo

                if not CODIGO_RE.fullmatch(
                    codigo
                ):
                    self.add_error(
                        "codigo",
                        (
                            "El código debe tener entre "
                            "2 y 15 caracteres, contener "
                            "al menos una letra y utilizar "
                            "únicamente letras, números "
                            "o guiones."
                        ),
                    )

        # ----------------------------------------------------
        # PERIODOS
        # ----------------------------------------------------
        elif self.modelo == "periodo":
            nombre = datos.get("name")

            if (
                nombre
                and not PERIODO_RE.fullmatch(nombre)
            ):
                self.add_error(
                    "name",
                    (
                        "El periodo debe tener el formato "
                        "AAAA-1 o AAAA-2. "
                        "Ejemplo: 2025-2."
                    ),
                )

            inicio = datos.get(
                "fecha_inicio"
            )

            fin = datos.get(
                "fecha_fin"
            )

            if (
                inicio
                and fin
                and fin < inicio
            ):
                self.add_error(
                    "fecha_fin",
                    (
                        "La fecha de fin no puede ser "
                        "anterior a la fecha de inicio."
                    ),
                )

        # ----------------------------------------------------
        # AULAS
        # ----------------------------------------------------
        elif self.modelo == "aula":
            for campo, etiqueta, maximo in (
                (
                    "name",
                    "El nombre del aula",
                    80,
                ),
                (
                    "edificio",
                    "El edificio",
                    100,
                ),
            ):
                valor = datos.get(campo)

                if valor:
                    try:
                        datos[campo] = (
                            validar_texto_con_letra(
                                valor,
                                etiqueta,
                                maximo=maximo,
                            )
                        )
                    except forms.ValidationError as error:
                        self.add_error(
                            campo,
                            error,
                        )

        return datos

    def datos_para_odoo(self):
        """
        Convierte fechas a formato ISO antes de enviarlas a Odoo.
        """
        datos = {}

        for nombre, valor in self.cleaned_data.items():
            if hasattr(valor, "isoformat"):
                valor = valor.isoformat()

            datos[nombre] = valor

        return datos
