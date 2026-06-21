from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from auditoria.utils import registrar_historial

from .forms import AusenciaIncapacidadForm
from .models import AusenciaIncapacidad


def es_htmx(request):

    return request.headers.get("HX-Request")


@login_required
def ausencias(request):

    registros = AusenciaIncapacidad.objects.all()

    template = "ausencias/ausencias.html"

    if es_htmx(request):

        template = "ausencias/ausencias_content.html"

    return render(
        request,
        template,
        {
            "registros": registros
        }
    )


@login_required
def ausencia_crear(request):

    if request.method == "POST":

        form = AusenciaIncapacidadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            registro = form.save()

            registrar_historial(
                request,
                "AUSENCIAS",
                "CREAR",
                (
                    f"Se registró {registro.get_tipo_display()} "
                    f"para {registro.empleado.nombre_completo}."
                )
            )

            registros = AusenciaIncapacidad.objects.all()

            response = render(
                request,
                "ausencias/ausencias_content.html",
                {
                    "registros": registros
                }
            )

            response["HX-Trigger"] = "cerrarModalInventario"

            return response

    else:

        form = AusenciaIncapacidadForm()

    return render(
        request,
        "ausencias/ausencia_form.html",
        {
            "form": form
        }
    )


@login_required
def ausencia_editar(request, id):

    registro = get_object_or_404(
        AusenciaIncapacidad,
        id=id
    )

    if request.method == "POST":

        form = AusenciaIncapacidadForm(
            request.POST,
            request.FILES,
            instance=registro
        )

        if form.is_valid():

            registro = form.save()

            registrar_historial(
                request,
                "AUSENCIAS",
                "EDITAR",
                (
                    f"Se editó {registro.get_tipo_display()} "
                    f"de {registro.empleado.nombre_completo}."
                )
            )

            registros = AusenciaIncapacidad.objects.all()

            response = render(
                request,
                "ausencias/ausencias_content.html",
                {
                    "registros": registros
                }
            )

            response["HX-Trigger"] = "cerrarModalInventario"

            return response

    else:

        form = AusenciaIncapacidadForm(
            instance=registro
        )

    return render(
        request,
        "ausencias/ausencia_form.html",
        {
            "form": form
        }
    )