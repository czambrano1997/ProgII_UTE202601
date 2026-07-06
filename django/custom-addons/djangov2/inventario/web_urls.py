from django.urls import path

from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('tienda/', views.tienda, name='tienda'),
    path('categorias-panel/', views.panel_categorias, name='panel_categorias'),
    path('clientes-panel/', views.panel_clientes, name='panel_clientes'),
    path('pedidos-panel/', views.panel_pedidos, name='panel_pedidos'),
]
