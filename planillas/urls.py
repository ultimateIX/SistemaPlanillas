from django.urls import path

from . import views
from . import pdf_views


urlpatterns = [

    path(
        "",
        views.planillas,
        name="planillas"
    ),

    path(
        "generar/",
        views.generar_planilla,
        name="generar_planilla"
    ),

    path(
        "detalle/<int:id>/",
        views.detalle_planilla,
        name="detalle_planilla"
    ),

    path(
        "historial/",
        views.historial_planillas,
        name="historial_planillas"
    ),

    path(
        "configuracion/",
        views.configuracion,
        name="configuracion"
    ),

    path(
        "isr/",
        views.isr,
        name="isr"
    ),

    path(
        "isr/crear/",
        views.isr_crear,
        name="isr_crear"
    ),

    path(
        "isr/editar/<int:id>/",
        views.isr_editar,
        name="isr_editar"
    ),

    path(
        "aguinaldo/",
        views.aguinaldo,
        name="aguinaldo"
    ),

    path(
        "aguinaldo/crear/",
        views.aguinaldo_crear,
        name="aguinaldo_crear"
    ),

    path(
        "aguinaldo/editar/<int:id>/",
        views.aguinaldo_editar,
        name="aguinaldo_editar"
    ),

    path(
        "cargar-tablas/",
        views.cargar_tablas_legales,
        name="cargar_tablas_legales"
    ),

    path(
        "pdf/general/<int:id>/",
        pdf_views.pdf_planilla_general,
        name="pdf_planilla_general"
    ),

    path(
        "pdf/boleta/<int:id>/",
        pdf_views.pdf_boleta_empleado,
        name="pdf_boleta_empleado"
    ),

]