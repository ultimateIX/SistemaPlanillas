from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import HistorialCambio


def es_htmx(request):

    return request.headers.get("HX-Request")


@login_required
def historial_cambios(request):

    cambios = HistorialCambio.objects.all()

    template = "auditoria/historial.html"

    if es_htmx(request):

        template = "auditoria/historial_content.html"

    return render(
        request,
        template,
        {
            "cambios": cambios
        }
    )