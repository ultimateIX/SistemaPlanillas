from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.asistencias,
        name="asistencias"
    ),

    path(
        "crear/",
        views.asistencia_crear,
        name="asistencia_crear"
    ),

    path(
        "editar/<int:id>/",
        views.asistencia_editar,
        name="asistencia_editar"
    ),

]