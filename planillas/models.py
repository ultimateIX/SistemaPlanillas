from django.db import models

from empleados.models import Empleado


# ==========================================
# CONFIGURACION GENERAL
# ==========================================

class ConfiguracionPlanilla(models.Model):

    porcentaje_isss_empleado = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=3.00
    )

    porcentaje_isss_patronal = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=7.50
    )

    porcentaje_afp_empleado = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=7.25
    )

    porcentaje_afp_patronal = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=8.75
    )

    tope_isss = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1000.00
    )

    aplicar_exencion_aguinaldo = models.BooleanField(
        default=True
    )

    limite_exento_aguinaldo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1500.00
    )

    porcentaje_quincena_25 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=50.00
    )

    antiguedad_minima_quincena_25 = models.IntegerField(
        default=1
    )

    class Meta:

        verbose_name = "Configuración Planilla"

        verbose_name_plural = (
            "Configuración Planilla"
        )

    def __str__(self):

        return "Configuración General"


# ==========================================
# TABLA ISR
# ==========================================

class TramoISR(models.Model):

    TIPOS_PERIODO = [

        ("QUINCENAL", "QUINCENAL"),

        ("MENSUAL", "MENSUAL"),

    ]

    periodo = models.CharField(
        max_length=20,
        choices=TIPOS_PERIODO,
        default="QUINCENAL"
    )

    desde = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    hasta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    porcentaje = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    exceso_sobre = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    cuota_fija = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    orden = models.IntegerField(
        default=1
    )

    class Meta:

        ordering = [
            "orden"
        ]

        verbose_name = "Tramo ISR"

        verbose_name_plural = (
            "Tramos ISR"
        )

    def __str__(self):

        return (
            f"{self.periodo} | "
            f"{self.desde} - "
            f"{self.hasta}"
        )


# ==========================================
# TABLA AGUINALDO
# ==========================================

class TramoAguinaldo(models.Model):

    antiguedad_desde = models.IntegerField()

    antiguedad_hasta = models.IntegerField(
        null=True,
        blank=True
    )

    dias_aguinaldo = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    orden = models.IntegerField(
        default=1
    )

    class Meta:

        ordering = [
            "orden"
        ]

        verbose_name = (
            "Tramo Aguinaldo"
        )

        verbose_name_plural = (
            "Tramos Aguinaldo"
        )

    def __str__(self):

        return (
            f"{self.antiguedad_desde} - "
            f"{self.antiguedad_hasta}"
        )


# ==========================================
# PLANILLA
# ==========================================

class Planilla(models.Model):

    fecha_generacion = models.DateTimeField(
        auto_now_add=True
    )

    periodo_inicio = models.DateField()

    periodo_fin = models.DateField()

    total_planilla = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    class Meta:

        ordering = [
            "-fecha_generacion"
        ]

    def __str__(self):

        return (
            f"Planilla {self.id}"
        )


# ==========================================
# DETALLE PLANILLA
# ==========================================

class DetallePlanilla(models.Model):

    planilla = models.ForeignKey(
        Planilla,
        on_delete=models.CASCADE,
        related_name="detalles"
    )

    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE
    )

    salario_quincenal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    horas_extra_diurnas = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    bonificaciones = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    vacaciones = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    aguinaldo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    aguinaldo_exento = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    aguinaldo_gravado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    quincena_25 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_devengado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    base_gravada_isr = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    isss_empleado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    afp_empleado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    renta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_descuentos = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    isss_patronal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    afp_patronal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    costo_patronal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    aplico_aguinaldo = models.BooleanField(
        default=False
    )

    aplico_quincena_25 = models.BooleanField(
        default=False
    )

    aplico_vacaciones = models.BooleanField(
        default=False
    )

    liquido_pagar = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    class Meta:

        ordering = [
            "empleado__nombre_completo"
        ]

    def __str__(self):

        return (
            f"{self.planilla.id} - "
            f"{self.empleado.nombre_completo}"
        )