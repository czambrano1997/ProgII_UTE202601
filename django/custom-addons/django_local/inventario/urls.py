# from django.urls import path
# from . import views
# 
# app_name = 'inventario'
# 
# urlpatterns = [
    # path('categorias/', views.lista_categoria, name='categorias'),
# ]
# 
from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('categorias/', views.lista_categoria, name='categoria'),
]