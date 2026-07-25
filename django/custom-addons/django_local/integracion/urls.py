from django.urls import path
from . import views

app_name = 'integracion'

urlpatterns = [
    # Carreras
    path('carrera/', views.carrera_lista, name='carrera_lista'),
    path('carrera/crear/', views.carrera_crear, name='carrera_crear'),
    path('carrera/eliminar/<int:pk>/', views.carrera_eliminar, name='carrera_eliminar'),

    # Periodos
    path('periodo/', views.periodo_lista, name='periodo_lista'),
    path('periodo/crear/', views.periodo_crear, name='periodo_crear'),
    path('periodo/eliminar/<int:pk>/', views.periodo_eliminar, name='periodo_eliminar'),

    # Aulas
    path('aula/', views.aula_lista, name='aula_lista'),
    path('aula/crear/', views.aula_crear, name='aula_crear'),
    path('aula/eliminar/<int:pk>/', views.aula_eliminar, name='aula_eliminar'),

    # Docentes
    path('teacher/', views.teacher_lista, name='teacher_lista'),
    path('teacher/crear/', views.teacher_crear, name='teacher_crear'),
    path('teacher/eliminar/<int:pk>/', views.teacher_eliminar, name='teacher_eliminar'),

    # Materias
    path('signature/', views.signature_lista, name='signature_lista'),
    path('signature/crear/', views.signature_crear, name='signature_crear'),
    path('signature/eliminar/<int:pk>/', views.signature_eliminar, name='signature_eliminar'),
]