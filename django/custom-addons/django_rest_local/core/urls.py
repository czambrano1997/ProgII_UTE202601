from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Enlaza las URLs de tu aplicación (cambia 'tienda' por 'inventario' si corresponde)
    path('api/', include('tienda.urls')), 
]
