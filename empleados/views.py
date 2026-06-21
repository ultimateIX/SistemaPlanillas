from django.shortcuts import render

from .forms import EmpleadoForm
from .models import Empleado


# ==========================================
# LISTAR EMPLEADOS
# ==========================================

def empleados(request):

    empleados = Empleado.objects.filter(
        activo=True
    )

    contexto = {
        "empleados": empleados
    }

    if request.headers.get("HX-Request"):

        return render(
            request,
            "empleados/lista_content.html",
            contexto
        )

    return render(
        request,
        "empleados/empleados.html",
        contexto
    )


# ==========================================
# CREAR EMPLEADO
# ==========================================

def empleado_crear(request):

    if request.method == "POST":

        form = EmpleadoForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            empleados = Empleado.objects.filter(
                activo=True
            )

            response = render(
                request,
                "empleados/lista_content.html",
                {
                    "empleados": empleados
                }
            )

            response["HX-Trigger"] = "empleadoGuardado"

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


# ==========================================
# EDITAR EMPLEADO
# ==========================================

def empleado_editar(request, id):

    empleado = Empleado.objects.get(
        id=id
    )

    if request.method == "POST":

        form = EmpleadoForm(
            request.POST,
            instance=empleado
        )

        if form.is_valid():

            form.save()

            empleados = Empleado.objects.filter(
                activo=True
            )

            response = render(
                request,
                "empleados/lista_content.html",
                {
                    "empleados": empleados
                }
            )

            response["HX-Trigger"] = "empleadoGuardado"

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


# ==========================================
# ELIMINAR EMPLEADO
# ==========================================

def empleado_eliminar(request, id):

    empleado = Empleado.objects.get(
        id=id
    )

    empleado.activo = False

    empleado.save()

    empleados = Empleado.objects.filter(
        activo=True
    )

    return render(
        request,
        "empleados/lista_content.html",
        {
            "empleados": empleados
        }
    )