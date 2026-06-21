from django.urls import path

from . import views

urlpatterns = [

    path(
        "",
        views.empleados,
        name="empleados"
    ),

    path(
        "crear/",
        views.empleado_crear,
        name="empleado_crear"
    ),
    path(
    "editar/<int:id>/",
    views.empleado_editar,
    name="empleado_editar"
),
path(
    "eliminar/<int:id>/",
    views.empleado_eliminar,
    name="empleado_eliminar"
),

]