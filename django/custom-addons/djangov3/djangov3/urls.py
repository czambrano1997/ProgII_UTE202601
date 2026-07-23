from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="integracion:inicio", permanent=False)),
    path("integracion/", include("integracion.urls")),
]
