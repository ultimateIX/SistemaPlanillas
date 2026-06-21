from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.ausencias,
        name="ausencias"
    ),

    path(
        "crear/",
        views.ausencia_crear,
        name="ausencia_crear"
    ),

    path(
        "editar/<int:id>/",
        views.ausencia_editar,
        name="ausencia_editar"
    ),

]