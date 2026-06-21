from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.shortcuts import render

from empleados.models import Empleado
from planillas.models import Planilla
from inventario.models import Producto, MovimientoInventario


@login_required
def dashboard(request):

    empleados_activos = Empleado.objects.filter(
        activo=True
    ).count()

    planillas_generadas = Planilla.objects.count()

    productos_total = Producto.objects.count()

    compras_total = MovimientoInventario.objects.filter(
        tipo="ENTRADA"
    ).count()

    ventas_total = MovimientoInventario.objects.filter(
        tipo="SALIDA"
    ).count()

    compras_por_mes = MovimientoInventario.objects.filter(
        tipo="ENTRADA"
    ).annotate(
        mes=ExtractMonth("fecha")
    ).values(
        "mes"
    ).annotate(
        total=Sum("cantidad")
    ).order_by(
        "mes"
    )

    ventas_por_mes = MovimientoInventario.objects.filter(
        tipo="SALIDA"
    ).annotate(
        mes=ExtractMonth("fecha")
    ).values(
        "mes"
    ).annotate(
        total=Sum("cantidad")
    ).order_by(
        "mes"
    )

    meses = [
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre",
    ]

    compras_data = [0] * 12
    ventas_data = [0] * 12

    for item in compras_por_mes:

        compras_data[item["mes"] - 1] = item["total"]

    for item in ventas_por_mes:

        ventas_data[item["mes"] - 1] = item["total"]

    contexto = {
        "empleados_activos": empleados_activos,
        "planillas_generadas": planillas_generadas,
        "productos_total": productos_total,
        "compras_total": compras_total,
        "ventas_total": ventas_total,
        "meses": meses,
        "compras_data": compras_data,
        "ventas_data": ventas_data,
    }

    if request.headers.get("HX-Request"):

        return render(
            request,
            "dashboard_content.html",
            contexto
        )

    return render(
        request,
        "dashboard.html",
        contexto
    )