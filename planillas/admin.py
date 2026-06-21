from django.contrib import admin

from .models import (
    ConfiguracionPlanilla,
    TramoISR,
    TramoAguinaldo,
    Planilla,
    DetallePlanilla
)


@admin.register(
    ConfiguracionPlanilla
)
class ConfiguracionPlanillaAdmin(
    admin.ModelAdmin
):

    list_display = (

        "porcentaje_isss_empleado",
        "porcentaje_isss_patronal",

        "porcentaje_afp_empleado",
        "porcentaje_afp_patronal",

        "tope_isss",

        "limite_exento_aguinaldo",

    )


@admin.register(
    TramoISR
)
class TramoISRAdmin(
    admin.ModelAdmin
):

    list_display = (

        "periodo",

        "desde",

        "hasta",

        "porcentaje",

        "exceso_sobre",

        "cuota_fija",

        "orden",

    )

    ordering = (
        "orden",
    )


@admin.register(
    TramoAguinaldo
)
class TramoAguinaldoAdmin(
    admin.ModelAdmin
):

    list_display = (

        "antiguedad_desde",

        "antiguedad_hasta",

        "dias_aguinaldo",

        "orden",

    )

    ordering = (
        "orden",
    )


class DetallePlanillaInline(
    admin.TabularInline
):

    model = DetallePlanilla

    extra = 0

    can_delete = False


@admin.register(
    Planilla
)
class PlanillaAdmin(
    admin.ModelAdmin
):

    list_display = (

        "id",

        "periodo_inicio",

        "periodo_fin",

        "fecha_generacion",

        "total_planilla",

    )

    inlines = [
        DetallePlanillaInline
    ]


@admin.register(
    DetallePlanilla
)
class DetallePlanillaAdmin(
    admin.ModelAdmin
):

    list_display = (

        "empleado",

        "salario_quincenal",

        "isss_empleado",

        "afp_empleado",

        "renta",

        "liquido_pagar",

    )

    list_filter = (

        "aplico_aguinaldo",

        "aplico_quincena_25",

        "aplico_vacaciones",

    )