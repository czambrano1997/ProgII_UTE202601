from django.urls import path
from . import views

urlpatterns = [
    # Carreras
    path('carreras/', views.lista_carreras, name='lista_carreras'),
    path('carreras/crear/', views.crear_carrera, name='crear_carrera'),
    path('carreras/eliminar/<int:carrera_id>/', views.eliminar_carrera, name='eliminar_carrera'),

    # Periodos
    path('periodos/', views.lista_periodos, name='lista_periodos'),
    path('periodos/crear/', views.crear_periodo, name='crear_periodo'),
    path('periodos/eliminar/<int:periodo_id>/', views.eliminar_periodo, name='eliminar_periodo'),

    # Aulas
    path('aulas/', views.lista_aulas, name='lista_aulas'),
    path('aulas/crear/', views.crear_aula, name='crear_aula'),
    path('aulas/eliminar/<int:aula_id>/', views.eliminar_aula, name='eliminar_aula'),

    # Materias 
    path('materias/', views.lista_materias, name='lista_materias'),
    path('materias/crear/', views.crear_materia, name='crear_materia'),
    path('materias/eliminar/<int:materia_id>/', views.eliminar_materia, name='eliminar_materia'),

    # Usuarios
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
]