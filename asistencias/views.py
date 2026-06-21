from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from auditoria.utils import registrar_historial

from .forms import AsistenciaForm
from .models import Asistencia


def es_htmx(request):

    return request.headers.get("HX-Request")


@login_required
def asistencias(request):

    asistencias = Asistencia.objects.all()

    template = "asistencias/asistencias.html"

    if es_htmx(request):

        template = "asistencias/asistencias_content.html"

    return render(
        request,
        template,
        {
            "asistencias": asistencias
        }
    )


@login_required
def asistencia_crear(request):

    if request.method == "POST":

        form = AsistenciaForm(
            request.POST
        )

        if form.is_valid():

            asistencia = form.save()

            registrar_historial(
                request,
                "ASISTENCIAS",
                "CREAR",
                (
                    f"Se registró asistencia de "
                    f"{asistencia.empleado.nombre_completo} "
                    f"con estado {asistencia.get_estado_display()}."
                )
            )

            asistencias = Asistencia.objects.all()

            response = render(
                request,
                "asistencias/asistencias_content.html",
                {
                    "asistencias": asistencias
                }
            )

            response["HX-Trigger"] = "cerrarModalInventario"

            return response

    else:

        form = AsistenciaForm()

    return render(
        request,
        "asistencias/asistencia_form.html",
        {
            "form": form
        }
    )


@login_required
def asistencia_editar(request, id):

    asistencia = get_object_or_404(
        Asistencia,
        id=id
    )

    if request.method == "POST":

        form = AsistenciaForm(
            request.POST,
            instance=asistencia
        )

        if form.is_valid():

            asistencia = form.save()

            registrar_historial(
                request,
                "ASISTENCIAS",
                "EDITAR",
                (
                    f"Se editó asistencia de "
                    f"{asistencia.empleado.nombre_completo} "
                    f"con estado {asistencia.get_estado_display()}."
                )
            )

            asistencias = Asistencia.objects.all()

            response = render(
                request,
                "asistencias/asistencias_content.html",
                {
                    "asistencias": asistencias
                }
            )

            response["HX-Trigger"] = "cerrarModalInventario"

            return response

    else:

        form = AsistenciaForm(
            instance=asistencia
        )

    return render(
        request,
        "asistencias/asistencia_form.html",
        {
            "form": form
        }
    )