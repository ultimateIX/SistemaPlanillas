from django.db import models

from empleados.models import Empleado


class AusenciaIncapacidad(models.Model):

    TIPO_CHOICES = [
        ("AUSENCIA", "Ausencia"),
        ("INCAPACIDAD", "Incapacidad"),
        ("PERMISO", "Permiso"),
        ("LLEGADA_TARDE", "Llegada tarde"),
    ]

    ESTADO_CHOICES = [
        ("REGISTRADO", "Registrado"),
        ("JUSTIFICADO", "Justificado"),
        ("NO_JUSTIFICADO", "No justificado"),
    ]

    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        related_name="ausencias_incapacidades"
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES
    )

    fecha_inicio = models.DateField()

    fecha_fin = models.DateField()

    motivo = models.CharField(
        max_length=200
    )

    observaciones = models.TextField(
        blank=True
    )

    documento = models.FileField(
        upload_to="incapacidades/",
        blank=True,
        null=True
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default="REGISTRADO"
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            "-fecha_registro"
        ]

    def __str__(self):

        return (
            f"{self.empleado.nombre_completo} - "
            f"{self.tipo}"
        )