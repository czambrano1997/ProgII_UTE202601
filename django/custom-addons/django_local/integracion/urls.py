from django.urls import path
from . import views

urlpatterns = [
    path('integracion/<str:model>/', views.lista, name='integracion_lista'),
    path('integracion/<str:model>/crear/', views.crear, name='integracion_crear'),
    path('integracion/<str:model>/eliminar/<int:record_id>/', views.eliminar, name='integracion_eliminar'),
]
