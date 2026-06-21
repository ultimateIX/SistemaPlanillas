from datetime import date
from datetime import timedelta
from decimal import Decimal

from django.shortcuts import get_object_or_404
from django.shortcuts import render

from auditoria.utils import registrar_historial

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


def es_htmx(request):

    return request.headers.get("HX-Request")


def calcular_isr_quincenal(base_gravada):

    if base_gravada <= Decimal("0.00"):

        return Decimal("0.00")

    tramo = TramoISR.objects.filter(
        periodo="QUINCENAL",
        desde__lte=base_gravada
    ).filter(
        hasta__gte=base_gravada
    ).first()

    if not tramo:

        tramo = TramoISR.objects.filter(
            periodo="QUINCENAL",
            desde__lte=base_gravada,
            hasta__isnull=True
        ).first()

    if not tramo:

        return Decimal("0.00")

    if tramo.porcentaje == 0:

        return Decimal("0.00")

    exceso = base_gravada - tramo.exceso_sobre

    renta = (
        tramo.cuota_fija
        + (
            exceso
            * (
                tramo.porcentaje
                / Decimal("100")
            )
        )
    )

    return round(
        renta,
        2
    )


def calcular_horas_extra_diurnas(empleado, cantidad_horas):

    if cantidad_horas <= Decimal("0.00"):

        return Decimal("0.00")

    if cantidad_horas > Decimal("88.00"):

        cantidad_horas = Decimal("88.00")

    salario_diario = (
        Decimal(empleado.salario_mensual)
        / Decimal("30")
    )

    salario_hora = (
        salario_diario
        / Decimal("8")
    )

    valor_hora_extra = (
        salario_hora
        * Decimal("2")
    )

    return round(
        valor_hora_extra * cantidad_horas,
        2
    )


def calcular_vacaciones(empleado, fecha_inicio, fecha_fin):

    fecha_ingreso = empleado.fecha_ingreso

    aniversario = date(
        fecha_fin.year,
        fecha_ingreso.month,
        fecha_ingreso.day
    )

    limite_pago = fecha_fin + timedelta(
        days=7
    )

    if aniversario < fecha_inicio:

        return Decimal("0.00"), False

    if aniversario > limite_pago:

        return Decimal("0.00"), False

    anios_laborados = (
        aniversario.year
        - fecha_ingreso.year
    )

    if anios_laborados < 1:

        return Decimal("0.00"), False

    ya_pagado = DetallePlanilla.objects.filter(
        empleado=empleado,
        aplico_vacaciones=True,
        planilla__periodo_inicio__year=fecha_inicio.year
    ).exists()

    if ya_pagado:

        return Decimal("0.00"), False

    salario_diario = round(
        Decimal(empleado.salario_mensual)
        / Decimal("30"),
        2
    )

    vacaciones_base = round(
        salario_diario * Decimal("15"),
        2
    )

    recargo_vacacional = round(
        vacaciones_base * Decimal("0.30"),
        2
    )

    total_vacaciones = round(
        vacaciones_base + recargo_vacacional,
        2
    )

    return total_vacaciones, True


def calcular_aguinaldo(empleado, fecha_inicio, fecha_fin, configuracion):

    if not (
        fecha_inicio.month == 12
        and fecha_inicio.day == 1
        and fecha_fin.month == 12
        and fecha_fin.day == 15
    ):

        return Decimal("0.00"), Decimal("0.00"), Decimal("0.00"), False

    ya_pagado = DetallePlanilla.objects.filter(
        empleado=empleado,
        aplico_aguinaldo=True,
        planilla__periodo_inicio__year=fecha_inicio.year
    ).exists()

    if ya_pagado:

        return Decimal("0.00"), Decimal("0.00"), Decimal("0.00"), False

    fecha_ingreso = empleado.fecha_ingreso

    dias_trabajados = (
        fecha_fin
        - fecha_ingreso
    ).days

    if dias_trabajados < 0:

        return Decimal("0.00"), Decimal("0.00"), Decimal("0.00"), False

    anios_laborados = (
        fecha_fin.year
        - fecha_ingreso.year
    )

    if (
        fecha_fin.month,
        fecha_fin.day
    ) < (
        fecha_ingreso.month,
        fecha_ingreso.day
    ):

        anios_laborados -= 1

    tramo = TramoAguinaldo.objects.filter(
        antiguedad_desde__lte=anios_laborados
    ).filter(
        antiguedad_hasta__gt=anios_laborados
    ).first()

    if not tramo:

        tramo = TramoAguinaldo.objects.filter(
            antiguedad_desde__lte=anios_laborados,
            antiguedad_hasta__isnull=True
        ).first()

    if tramo:

        dias_aguinaldo = tramo.dias_aguinaldo

    else:

        dias_aguinaldo = Decimal("15.00")

    if anios_laborados < 1:

        dias_aguinaldo = round(
            (
                Decimal(dias_trabajados)
                / Decimal("365")
            )
            * dias_aguinaldo,
            2
        )

    salario_diario = round(
        Decimal(empleado.salario_mensual)
        / Decimal("30"),
        2
    )

    aguinaldo = round(
        salario_diario * dias_aguinaldo,
        2
    )

    if configuracion.aplicar_exencion_aguinaldo:

        aguinaldo_exento = min(
            aguinaldo,
            configuracion.limite_exento_aguinaldo
        )

        aguinaldo_gravado = max(
            aguinaldo - configuracion.limite_exento_aguinaldo,
            Decimal("0.00")
        )

    else:

        aguinaldo_exento = Decimal("0.00")

        aguinaldo_gravado = aguinaldo

    return aguinaldo, aguinaldo_exento, aguinaldo_gravado, True


def calcular_quincena_25(empleado, fecha_inicio, fecha_fin, configuracion):

    if not (
        fecha_inicio.month == 1
        and fecha_inicio.day == 1
        and fecha_fin.month == 1
        and fecha_fin.day == 15
    ):

        return Decimal("0.00"), False

    if Decimal(empleado.salario_mensual) > Decimal("1500.00"):

        return Decimal("0.00"), False

    fecha_ingreso = empleado.fecha_ingreso

    anios_laborados = (
        fecha_inicio.year
        - fecha_ingreso.year
    )

    if (
        fecha_inicio.month,
        fecha_inicio.day
    ) < (
        fecha_ingreso.month,
        fecha_ingreso.day
    ):

        anios_laborados -= 1

    if anios_laborados < configuracion.antiguedad_minima_quincena_25:

        return Decimal("0.00"), False

    ya_pagado = DetallePlanilla.objects.filter(
        empleado=empleado,
        aplico_quincena_25=True,
        planilla__periodo_inicio__year=fecha_inicio.year
    ).exists()

    if ya_pagado:

        return Decimal("0.00"), False

    quincena_25 = round(
        Decimal(empleado.salario_mensual)
        * (
            configuracion.porcentaje_quincena_25
            / Decimal("100")
        ),
        2
    )

    return quincena_25, True


def planillas(request):

    planillas = Planilla.objects.all()

    empleados = Empleado.objects.filter(
        activo=True
    )

    contexto = {
        "planillas": planillas,
        "empleados": empleados
    }

    if es_htmx(request):

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


def generar_planilla(request):

    inicio = request.GET.get("inicio")
    fin = request.GET.get("fin")

    if not inicio or not fin:

        return render(
            request,
            "planillas/lista_content.html",
            {
                "planillas": Planilla.objects.all(),
                "empleados": Empleado.objects.filter(
                    activo=True
                )
            }
        )

    fecha_inicio = date.fromisoformat(
        inicio
    )

    fecha_fin = date.fromisoformat(
        fin
    )

    configuracion = ConfiguracionPlanilla.objects.first()

    if not configuracion:

        configuracion = ConfiguracionPlanilla.objects.create()

    empleados = Empleado.objects.filter(
        activo=True
    )

    empleados_con_horas_extra = request.GET.getlist(
        "empleados_horas_extra"
    )

    planilla = Planilla.objects.create(
        periodo_inicio=inicio,
        periodo_fin=fin,
        total_planilla=0
    )

    total_planilla = Decimal("0.00")

    for empleado in empleados:

        salario_quincenal = round(
            Decimal(empleado.salario_mensual)
            / Decimal("2"),
            2
        )

        horas_extra = Decimal("0.00")

        if str(empleado.id) in empleados_con_horas_extra:

            horas_extra_texto = request.GET.get(
                f"horas_extra_{empleado.id}",
                "0"
            )

            try:

                cantidad_horas = Decimal(
                    horas_extra_texto
                )

            except:

                cantidad_horas = Decimal("0.00")

            horas_extra = calcular_horas_extra_diurnas(
                empleado,
                cantidad_horas
            )

        bonificaciones = Decimal("0.00")

        vacaciones, aplico_vacaciones = calcular_vacaciones(
            empleado,
            fecha_inicio,
            fecha_fin
        )

        (
            aguinaldo,
            aguinaldo_exento,
            aguinaldo_gravado,
            aplico_aguinaldo
        ) = calcular_aguinaldo(
            empleado,
            fecha_inicio,
            fecha_fin,
            configuracion
        )

        quincena_25, aplico_quincena_25 = calcular_quincena_25(
            empleado,
            fecha_inicio,
            fecha_fin,
            configuracion
        )

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
            base_isss / Decimal("2"),
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
            )
            - isss_empleado
            - afp_empleado,
            2
        )

        renta_normal = calcular_isr_quincenal(
            base_gravada_isr
        )

        renta_aguinaldo = calcular_isr_quincenal(
            aguinaldo_gravado
        )

        renta = round(
            renta_normal + renta_aguinaldo,
            2
        )

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
            aplico_aguinaldo=aplico_aguinaldo,
            aplico_quincena_25=aplico_quincena_25,
            aplico_vacaciones=aplico_vacaciones,
            liquido_pagar=liquido_pagar
        )

        total_planilla += liquido_pagar

    planilla.total_planilla = total_planilla

    planilla.save()

    registrar_historial(
        request,
        "PLANILLAS",
        "GENERAR",
        (
            f"Se generó planilla del período "
            f"{fecha_inicio.strftime('%d/%m/%Y')} al "
            f"{fecha_fin.strftime('%d/%m/%Y')}."
        )
    )

    return render(
        request,
        "planillas/lista_content.html",
        {
            "planillas": Planilla.objects.all(),
            "empleados": Empleado.objects.filter(
                activo=True
            )
        }
    )


def detalle_planilla(request, id):

    planilla = get_object_or_404(
        Planilla,
        id=id
    )

    detalles = DetallePlanilla.objects.filter(
        planilla=planilla
    )

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

        totales["salario_quincenal"] += detalle.salario_quincenal
        totales["horas_extra_diurnas"] += detalle.horas_extra_diurnas
        totales["vacaciones"] += detalle.vacaciones
        totales["aguinaldo"] += detalle.aguinaldo
        totales["quincena_25"] += detalle.quincena_25
        totales["total_devengado"] += detalle.total_devengado
        totales["isss_empleado"] += detalle.isss_empleado
        totales["afp_empleado"] += detalle.afp_empleado
        totales["renta"] += detalle.renta
        totales["total_descuentos"] += detalle.total_descuentos
        totales["liquido_pagar"] += detalle.liquido_pagar
        totales["isss_patronal"] += detalle.isss_patronal
        totales["afp_patronal"] += detalle.afp_patronal
        totales["costo_patronal"] += detalle.costo_patronal

    return render(
        request,
        "planillas/detalle_planilla.html",
        {
            "planilla": planilla,
            "detalles": detalles,
            "totales": totales
        }
    )


def historial_planillas(request):

    return render(
        request,
        "planillas/historial.html",
        {
            "planillas": Planilla.objects.all()
        }
    )


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

            registrar_historial(
                request,
                "CONFIGURACION",
                "EDITAR",
                "Se actualizó la configuración general de planillas."
            )

    else:

        form = ConfiguracionPlanillaForm(
            instance=configuracion
        )

    template = "planillas/configuracion.html"

    if es_htmx(request):

        template = "planillas/configuracion_content.html"

    return render(
        request,
        template,
        {
            "form": form
        }
    )


def isr(request):

    tramos = TramoISR.objects.all()

    template = "planillas/isr.html"

    if es_htmx(request):

        template = "planillas/isr_content.html"

    return render(
        request,
        template,
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

            tramo = form.save()

            registrar_historial(
                request,
                "CONFIGURACION",
                "CREAR",
                (
                    f"Se creó tramo ISR desde "
                    f"{tramo.desde} hasta {tramo.hasta}."
                )
            )

            return render(
                request,
                "planillas/isr_content.html",
                {
                    "tramos": TramoISR.objects.all()
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

            tramo = form.save()

            registrar_historial(
                request,
                "CONFIGURACION",
                "EDITAR",
                (
                    f"Se editó tramo ISR desde "
                    f"{tramo.desde} hasta {tramo.hasta}."
                )
            )

            return render(
                request,
                "planillas/isr_content.html",
                {
                    "tramos": TramoISR.objects.all()
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


def aguinaldo(request):

    tramos = TramoAguinaldo.objects.all()

    template = "planillas/aguinaldo.html"

    if es_htmx(request):

        template = "planillas/aguinaldo_content.html"

    return render(
        request,
        template,
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

            tramo = form.save()

            registrar_historial(
                request,
                "CONFIGURACION",
                "CREAR",
                (
                    f"Se creó tramo de aguinaldo "
                    f"con {tramo.dias_aguinaldo} días."
                )
            )

            return render(
                request,
                "planillas/aguinaldo_content.html",
                {
                    "tramos": TramoAguinaldo.objects.all()
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

            tramo = form.save()

            registrar_historial(
                request,
                "CONFIGURACION",
                "EDITAR",
                (
                    f"Se editó tramo de aguinaldo "
                    f"con {tramo.dias_aguinaldo} días."
                )
            )

            return render(
                request,
                "planillas/aguinaldo_content.html",
                {
                    "tramos": TramoAguinaldo.objects.all()
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

    registrar_historial(
        request,
        "CONFIGURACION",
        "REGISTRAR",
        "Se cargaron las tablas legales por defecto."
    )

    configuracion = ConfiguracionPlanilla.objects.first()

    if not configuracion:

        configuracion = ConfiguracionPlanilla.objects.create()

    form = ConfiguracionPlanillaForm(
        instance=configuracion
    )

    template = "planillas/configuracion.html"

    if es_htmx(request):

        template = "planillas/configuracion_content.html"

    return render(
        request,
        template,
        {
            "form": form
        }
    )