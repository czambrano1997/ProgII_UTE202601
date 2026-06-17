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
    path('categoria/', views.lista_categoria, name='categoria'),
    path('producto/', views.lista_productos, name='lista_productos'),  # ← nueva
    path('artes/', views.lista_arte, name='lista_arte'),

]