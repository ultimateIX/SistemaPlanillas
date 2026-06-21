from django.db import models

from empleados.models import Empleado


class Asistencia(models.Model):

    ESTADO_CHOICES = [
        ("PRESENTE", "Presente"),
        ("AUSENTE", "Ausente"),
        ("PERMISO", "Permiso"),
        ("INCAPACIDAD", "Incapacidad"),
        ("VACACION", "Vacación"),
    ]

    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        related_name="asistencias"
    )

    fecha = models.DateField()

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default="PRESENTE"
    )

    observacion = models.TextField(
        blank=True
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            "-fecha",
            "empleado__nombre_completo"
        ]

    def __str__(self):

        return (
            f"{self.empleado.nombre_completo} - "
            f"{self.fecha} - "
            f"{self.estado}"
        )