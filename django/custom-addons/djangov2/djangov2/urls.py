from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('inventario.web_urls')),
    path('admin/', admin.site.urls),
    path('api/', include('inventario.urls')),
]
