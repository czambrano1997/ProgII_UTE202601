from django.urls import path

from . import views

app_name = "integracion"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("<slug:modelo>/", views.lista, name="lista"),
    path("<slug:modelo>/crear/", views.crear, name="crear"),
    path("<slug:modelo>/eliminar/<int:registro_id>/", views.eliminar, name="eliminar"),
]
