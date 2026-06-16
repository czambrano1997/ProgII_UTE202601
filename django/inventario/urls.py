from django.urls import path
from . import views

urlpatterns = [
    path('cateforias/', views.lista_categoria, name='lista_categoria'),
]
