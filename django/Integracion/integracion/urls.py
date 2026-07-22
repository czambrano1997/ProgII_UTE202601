from django.urls import path
from . import views

app_name = 'integracion'

urlpatterns = [
    path('<str:modelo>/', views.lista, name='lista'),
    path('<str:modelo>/crear/', views.crear, name='crear'),
    path('<str:modelo>/eliminar/<int:registro_id>/', views.confirmar_eliminar, name='confirmar_eliminar'),
]