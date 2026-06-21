from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from empleados.models import Empleado
from planillas.models import Planilla


@login_required
def dashboard(request):

    empleados_activos = Empleado.objects.filter(
        activo=True
    ).count()

    planillas_generadas = Planilla.objects.count()

    ultima_planilla = Planilla.objects.order_by(
        "-fecha_generacion"
    ).first()

    total_ultima_planilla = 0

    if ultima_planilla:

        total_ultima_planilla = ultima_planilla.total_planilla

    contexto = {
        "empleados_activos": empleados_activos,
        "planillas_generadas": planillas_generadas,
        "total_ultima_planilla": total_ultima_planilla,
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