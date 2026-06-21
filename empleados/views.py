from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from auditoria.utils import registrar_historial

from .forms import EmpleadoForm
from .models import Empleado


def es_htmx(request):

    return request.headers.get("HX-Request")


@login_required
def empleados(request):

    empleados = Empleado.objects.all()

    template = "empleados/empleados.html"

    if es_htmx(request):

        template = "empleados/lista_content.html"

    return render(
        request,
        template,
        {
            "empleados": empleados
        }
    )


@login_required
def empleado_crear(request):

    if request.method == "POST":

        form = EmpleadoForm(
            request.POST
        )

        if form.is_valid():

            empleado = form.save()

            registrar_historial(
                request,
                "EMPLEADOS",
                "CREAR",
                f"Se creó el empleado {empleado.nombre_completo}."
            )

            empleados = Empleado.objects.all()

            response = render(
                request,
                "empleados/lista_content.html",
                {
                    "empleados": empleados
                }
            )

            response["HX-Trigger"] = "cerrarModalInventario"

            return response

    else:

        form = EmpleadoForm()

    return render(
        request,
        "empleados/empleado_form.html",
        {
            "form": form
        }
    )


@login_required
def empleado_editar(request, id):

    empleado = get_object_or_404(
        Empleado,
        id=id
    )

    if request.method == "POST":

        form = EmpleadoForm(
            request.POST,
            instance=empleado
        )

        if form.is_valid():

            empleado = form.save()

            registrar_historial(
                request,
                "EMPLEADOS",
                "EDITAR",
                f"Se editó el empleado {empleado.nombre_completo}."
            )

            empleados = Empleado.objects.all()

            response = render(
                request,
                "empleados/lista_content.html",
                {
                    "empleados": empleados
                }
            )

            response["HX-Trigger"] = "cerrarModalInventario"

            return response

    else:

        form = EmpleadoForm(
            instance=empleado
        )

    return render(
        request,
        "empleados/empleado_form.html",
        {
            "form": form
        }
    )


@login_required
def empleado_eliminar(request, id):

    empleado = get_object_or_404(
        Empleado,
        id=id
    )

    empleado.activo = False

    empleado.save()

    registrar_historial(
        request,
        "EMPLEADOS",
        "ELIMINAR",
        f"Se desactivó el empleado {empleado.nombre_completo}."
    )

    empleados = Empleado.objects.all()

    return render(
        request,
        "empleados/lista_content.html",
        {
            "empleados": empleados
        }
    )