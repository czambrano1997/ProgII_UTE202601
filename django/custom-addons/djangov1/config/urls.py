from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api/', include('djangov2.urls')),
    path("admin/", admin.site.urls),
    path("", include("djangov1.urls")),
]
