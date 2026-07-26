from django.urls import path

from . import views

app_name = "tienda"

urlpatterns = [
    path("categoria/", views.lista_categoria, name="categoria"),
    path("producto/", views.lista_productos, name="lista_productos"),
]
