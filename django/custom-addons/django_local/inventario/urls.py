from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('proveedores/', views.vista_proveedores, name='proveedores'),
    path('categorias/', views.vista_categorias, name='categorias'),
]