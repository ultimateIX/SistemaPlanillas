from django.urls import path

from . import views


urlpatterns = [

    path(
        "productos/",
        views.productos,
        name="productos"
    ),

    path(
        "productos/crear/",
        views.producto_crear,
        name="producto_crear"
    ),

    path(
        "productos/editar/<int:id>/",
        views.producto_editar,
        name="producto_editar"
    ),

    path(
        "compras/",
        views.compras,
        name="compras"
    ),

    path(
        "compras/registrar/",
        views.registrar_compra,
        name="registrar_compra"
    ),

    path(
        "ventas/",
        views.ventas,
        name="ventas"
    ),

    path(
        "ventas/registrar/",
        views.registrar_venta,
        name="registrar_venta"
    ),

    path(
        "historial-movimientos/",
        views.historial_movimientos,
        name="historial_movimientos"
    ),

]