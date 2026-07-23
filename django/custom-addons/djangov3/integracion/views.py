from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from .config import MODELOS, obtener_config
from .forms import RegistroOdooForm
from .odoo_client import OdooClientError, crear_registro, eliminar_registro, obtener_todos


def _config_o_404(modelo):
    config = obtener_config(modelo)
    if config is None:
        raise Http404("Modelo de integración no encontrado.")
    return config


def _mostrar_valor(value):
    if value is True:
        return "Sí"
    if value is False:
        return "No"
    if value in (None, ""):
        return "—"
    return value


def inicio(request):
    return render(request, "integracion/inicio.html", {"modelos": MODELOS})


def lista(request, modelo):
    config = _config_o_404(modelo)
    registros = []
    try:
        registros = obtener_todos(modelo)
    except OdooClientError as exc:
        messages.error(request, str(exc))

    filas = []
    for registro in registros:
        filas.append({
            "id": registro.get("id"),
            "valores": [_mostrar_valor(registro.get(campo["name"])) for campo in config["campos"]],
        })

    return render(request, "integracion/lista.html", {
        "modelo": modelo,
        "config": config,
        "filas": filas,
    })


def crear(request, modelo):
    config = _config_o_404(modelo)
    form = RegistroOdooForm(request.POST or None, modelo=modelo)
    if request.method == "POST" and form.is_valid():
        try:
            result = crear_registro(modelo, form.datos_para_odoo())
        except OdooClientError as exc:
            messages.error(request, str(exc))
        else:
            messages.success(request, result.get("message", f"{config['singular']} creado correctamente."))
            return redirect("integracion:lista", modelo=modelo)

    return render(request, "integracion/form.html", {
        "modelo": modelo,
        "config": config,
        "form": form,
    })


def eliminar(request, modelo, registro_id):
    config = _config_o_404(modelo)
    if request.method == "POST":
        try:
            result = eliminar_registro(modelo, registro_id)
        except OdooClientError as exc:
            messages.error(request, str(exc))
        else:
            messages.success(request, result.get("message", f"{config['singular']} eliminado correctamente."))
        return redirect("integracion:lista", modelo=modelo)

    return render(request, "integracion/confirmar_eliminar.html", {
        "modelo": modelo,
        "config": config,
        "registro_id": registro_id,
    })
