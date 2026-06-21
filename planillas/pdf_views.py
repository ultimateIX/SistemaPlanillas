from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template

from xhtml2pdf import pisa

from .models import (
    DetallePlanilla,
    Planilla
)


def link_callback(uri, rel):

    if uri.startswith(settings.STATIC_URL):

        path = uri.replace(
            settings.STATIC_URL,
            ""
        )

        for static_dir in settings.STATICFILES_DIRS:

            full_path = Path(static_dir) / path

            if full_path.exists():

                return str(full_path)

    return uri


def calcular_totales(detalles):

    totales = {
        "salario_quincenal": Decimal("0.00"),
        "horas_extra_diurnas": Decimal("0.00"),
        "vacaciones": Decimal("0.00"),
        "aguinaldo": Decimal("0.00"),
        "quincena_25": Decimal("0.00"),
        "total_devengado": Decimal("0.00"),
        "isss_empleado": Decimal("0.00"),
        "afp_empleado": Decimal("0.00"),
        "renta": Decimal("0.00"),
        "total_descuentos": Decimal("0.00"),
        "liquido_pagar": Decimal("0.00"),
        "isss_patronal": Decimal("0.00"),
        "afp_patronal": Decimal("0.00"),
        "costo_patronal": Decimal("0.00"),
    }

    for detalle in detalles:

        for campo in totales:

            totales[campo] += getattr(
                detalle,
                campo
            )

    return totales


def generar_pdf(template_name, context, filename):

    template = get_template(
        template_name
    )

    html = template.render(
        context
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{filename}"'
    )

    pisa_status = pisa.CreatePDF(
        html,
        dest=response,
        link_callback=link_callback
    )

    if pisa_status.err:

        return HttpResponse(
            "Error al generar PDF",
            status=500
        )

    return response


def pdf_planilla_general(request, id):

    planilla = get_object_or_404(
        Planilla,
        id=id
    )

    detalles = DetallePlanilla.objects.filter(
        planilla=planilla
    )

    return generar_pdf(
        "planillas/pdf_planilla_general.html",
        {
            "planilla": planilla,
            "detalles": detalles,
            "totales": calcular_totales(detalles),
        },
        f"planilla_general_{planilla.id}.pdf"
    )


def pdf_boleta_empleado(request, id):

    detalle = get_object_or_404(
        DetallePlanilla,
        id=id
    )

    return generar_pdf(
        "planillas/pdf_boleta_empleado.html",
        {
            "detalle": detalle,
            "empleado": detalle.empleado,
            "planilla": detalle.planilla,
        },
        f"boleta_{detalle.empleado.nombre_completo}_{detalle.planilla.id}.pdf"
    )