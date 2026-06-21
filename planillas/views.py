from decimal import Decimal

from django.shortcuts import get_object_or_404
from django.shortcuts import render

from empleados.models import Empleado

from .forms import (
    ConfiguracionPlanillaForm,
    TramoAguinaldoForm,
    TramoISRForm,
)

from .models import (
    ConfiguracionPlanilla,
    DetallePlanilla,
    Planilla,
    TramoAguinaldo,
    TramoISR,
)


# ==========================================
# PLANILLAS
# ==========================================

def planillas(request):

    planillas = Planilla.objects.all()

    contexto = {
        "planillas": planillas
    }

    if request.headers.get("HX-Request"):

        return render(
            request,
            "planillas/lista_content.html",
            contexto
        )

    return render(
        request,
        "planillas/planillas.html",
        contexto
    )


# ==========================================
# GENERAR PLANILLA
# ==========================================

def generar_planilla(request):

    inicio = request.GET.get("inicio")

    fin = request.GET.get("fin")

    if not inicio or not fin:

        return render(
            request,
            "planillas/lista_content.html",
            {
                "planillas": Planilla.objects.all()
            }
        )

    configuracion = ConfiguracionPlanilla.objects.first()

    if not configuracion:

        configuracion = ConfiguracionPlanilla.objects.create()

    empleados = Empleado.objects.filter(
        activo=True
    )

    planilla = Planilla.objects.create(
        periodo_inicio=inicio,
        periodo_fin=fin,
        total_planilla=0
    )

    total_planilla = Decimal("0.00")

    for empleado in empleados:

        salario_quincenal = round(
            Decimal(empleado.salario_mensual) / 2,
            2
        )

        horas_extra = Decimal("0.00")

        bonificaciones = Decimal("0.00")

        vacaciones = Decimal("0.00")

        aguinaldo = Decimal("0.00")

        aguinaldo_exento = Decimal("0.00")

        aguinaldo_gravado = Decimal("0.00")

        quincena_25 = Decimal("0.00")

        total_devengado = (
            salario_quincenal
            + horas_extra
            + bonificaciones
            + vacaciones
            + aguinaldo
            + quincena_25
        )

        base_isss = min(
            Decimal(empleado.salario_mensual),
            configuracion.tope_isss
        )

        base_isss_quincenal = round(
            base_isss / 2,
            2
        )

        isss_empleado = round(
            base_isss_quincenal
            * (
                configuracion.porcentaje_isss_empleado
                / Decimal("100")
            ),
            2
        )

        isss_patronal = round(
            base_isss_quincenal
            * (
                configuracion.porcentaje_isss_patronal
                / Decimal("100")
            ),
            2
        )

        afp_empleado = round(
            salario_quincenal
            * (
                configuracion.porcentaje_afp_empleado
                / Decimal("100")
            ),
            2
        )

        afp_patronal = round(
            salario_quincenal
            * (
                configuracion.porcentaje_afp_patronal
                / Decimal("100")
            ),
            2
        )

        base_gravada_isr = round(
            (
                salario_quincenal
                + horas_extra
                + bonificaciones
                + vacaciones
                + aguinaldo_gravado
            )
            - isss_empleado
            - afp_empleado,
            2
        )

        renta = Decimal("0.00")

        total_descuentos = (
            isss_empleado
            + afp_empleado
            + renta
        )

        liquido_pagar = round(
            total_devengado - total_descuentos,
            2
        )

        costo_patronal = round(
            total_devengado
            + isss_patronal
            + afp_patronal,
            2
        )

        DetallePlanilla.objects.create(
            planilla=planilla,
            empleado=empleado,
            salario_quincenal=salario_quincenal,
            horas_extra_diurnas=horas_extra,
            bonificaciones=bonificaciones,
            vacaciones=vacaciones,
            aguinaldo=aguinaldo,
            aguinaldo_exento=aguinaldo_exento,
            aguinaldo_gravado=aguinaldo_gravado,
            quincena_25=quincena_25,
            total_devengado=total_devengado,
            base_gravada_isr=base_gravada_isr,
            isss_empleado=isss_empleado,
            afp_empleado=afp_empleado,
            renta=renta,
            total_descuentos=total_descuentos,
            isss_patronal=isss_patronal,
            afp_patronal=afp_patronal,
            costo_patronal=costo_patronal,
            aplico_aguinaldo=False,
            aplico_quincena_25=False,
            aplico_vacaciones=False,
            liquido_pagar=liquido_pagar
        )

        total_planilla += liquido_pagar

    planilla.total_planilla = total_planilla

    planilla.save()

    return render(
        request,
        "planillas/lista_content.html",
        {
            "planillas": Planilla.objects.all()
        }
    )


# ==========================================
# DETALLE PLANILLA
# ==========================================

def detalle_planilla(request, id):

    planilla = get_object_or_404(
        Planilla,
        id=id
    )

    detalles = DetallePlanilla.objects.filter(
        planilla=planilla
    )

    return render(
        request,
        "planillas/detalle_planilla.html",
        {
            "planilla": planilla,
            "detalles": detalles
        }
    )


# ==========================================
# HISTORIAL
# ==========================================

def historial_planillas(request):

    return render(
        request,
        "planillas/historial.html",
        {
            "planillas": Planilla.objects.all()
        }
    )


# ==========================================
# CONFIGURACION GENERAL
# ==========================================

def configuracion(request):

    configuracion = ConfiguracionPlanilla.objects.first()

    if not configuracion:

        configuracion = ConfiguracionPlanilla.objects.create()

    if request.method == "POST":

        form = ConfiguracionPlanillaForm(
            request.POST,
            instance=configuracion
        )

        if form.is_valid():

            form.save()

    else:

        form = ConfiguracionPlanillaForm(
            instance=configuracion
        )

    return render(
        request,
        "planillas/configuracion.html",
        {
            "form": form
        }
    )


# ==========================================
# ISR
# ==========================================

def isr(request):

    tramos = TramoISR.objects.all()

    return render(
        request,
        "planillas/isr.html",
        {
            "tramos": tramos
        }
    )


def isr_crear(request):

    if request.method == "POST":

        form = TramoISRForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            tramos = TramoISR.objects.all()

            return render(
                request,
                "planillas/isr.html",
                {
                    "tramos": tramos
                }
            )

    else:

        form = TramoISRForm()

    return render(
        request,
        "planillas/isr_form.html",
        {
            "form": form
        }
    )


def isr_editar(request, id):

    tramo = get_object_or_404(
        TramoISR,
        id=id
    )

    if request.method == "POST":

        form = TramoISRForm(
            request.POST,
            instance=tramo
        )

        if form.is_valid():

            form.save()

            tramos = TramoISR.objects.all()

            return render(
                request,
                "planillas/isr.html",
                {
                    "tramos": tramos
                }
            )

    else:

        form = TramoISRForm(
            instance=tramo
        )

    return render(
        request,
        "planillas/isr_form.html",
        {
            "form": form
        }
    )


# ==========================================
# AGUINALDO
# ==========================================

def aguinaldo(request):

    tramos = TramoAguinaldo.objects.all()

    return render(
        request,
        "planillas/aguinaldo.html",
        {
            "tramos": tramos
        }
    )


def aguinaldo_crear(request):

    if request.method == "POST":

        form = TramoAguinaldoForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            tramos = TramoAguinaldo.objects.all()

            return render(
                request,
                "planillas/aguinaldo.html",
                {
                    "tramos": tramos
                }
            )

    else:

        form = TramoAguinaldoForm()

    return render(
        request,
        "planillas/aguinaldo_form.html",
        {
            "form": form
        }
    )


def aguinaldo_editar(request, id):

    tramo = get_object_or_404(
        TramoAguinaldo,
        id=id
    )

    if request.method == "POST":

        form = TramoAguinaldoForm(
            request.POST,
            instance=tramo
        )

        if form.is_valid():

            form.save()

            tramos = TramoAguinaldo.objects.all()

            return render(
                request,
                "planillas/aguinaldo.html",
                {
                    "tramos": tramos
                }
            )

    else:

        form = TramoAguinaldoForm(
            instance=tramo
        )

    return render(
        request,
        "planillas/aguinaldo_form.html",
        {
            "form": form
        }
    )


# ==========================================
# CARGAR TABLAS LEGALES
# ==========================================

def cargar_tablas_legales(request):

    if not TramoISR.objects.exists():

        TramoISR.objects.create(
            periodo="QUINCENAL",
            desde=Decimal("0.01"),
            hasta=Decimal("275.00"),
            porcentaje=Decimal("0.00"),
            exceso_sobre=Decimal("0.00"),
            cuota_fija=Decimal("0.00"),
            orden=1
        )

        TramoISR.objects.create(
            periodo="QUINCENAL",
            desde=Decimal("275.01"),
            hasta=Decimal("447.62"),
            porcentaje=Decimal("10.00"),
            exceso_sobre=Decimal("275.00"),
            cuota_fija=Decimal("8.83"),
            orden=2
        )

        TramoISR.objects.create(
            periodo="QUINCENAL",
            desde=Decimal("447.63"),
            hasta=Decimal("1019.05"),
            porcentaje=Decimal("20.00"),
            exceso_sobre=Decimal("447.62"),
            cuota_fija=Decimal("30.00"),
            orden=3
        )

        TramoISR.objects.create(
            periodo="QUINCENAL",
            desde=Decimal("1019.06"),
            hasta=None,
            porcentaje=Decimal("30.00"),
            exceso_sobre=Decimal("1019.05"),
            cuota_fija=Decimal("144.28"),
            orden=4
        )

    if not TramoAguinaldo.objects.exists():

        TramoAguinaldo.objects.create(
            antiguedad_desde=0,
            antiguedad_hasta=1,
            dias_aguinaldo=Decimal("15.00"),
            orden=1
        )

        TramoAguinaldo.objects.create(
            antiguedad_desde=1,
            antiguedad_hasta=3,
            dias_aguinaldo=Decimal("15.00"),
            orden=2
        )

        TramoAguinaldo.objects.create(
            antiguedad_desde=3,
            antiguedad_hasta=10,
            dias_aguinaldo=Decimal("19.00"),
            orden=3
        )

        TramoAguinaldo.objects.create(
            antiguedad_desde=10,
            antiguedad_hasta=None,
            dias_aguinaldo=Decimal("21.00"),
            orden=4
        )

    configuracion = ConfiguracionPlanilla.objects.first()

    if not configuracion:

        configuracion = ConfiguracionPlanilla.objects.create()

    form = ConfiguracionPlanillaForm(
        instance=configuracion
    )

    return render(
        request,
        "planillas/configuracion.html",
        {
            "form": form
        }
    )