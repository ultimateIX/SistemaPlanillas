from django.db import models
from datetime import date

class Empleado(models.Model):

    dui = models.CharField(
        max_length=10,
        unique=True
    )

    numero_isss = models.CharField(
        max_length=20,
        unique=True
    )

    telefono = models.CharField(
        max_length=20
    )

    nombre_completo = models.CharField(
        max_length=200
    )

    correo = models.EmailField(
        blank=True
    )

    cargo = models.CharField(
        max_length=100,
        blank=True
    )

    fecha_ingreso = models.DateField()

    salario_mensual = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    activo = models.BooleanField(
        default=True
    )

    class Meta:

        ordering = ["nombre_completo"]

        verbose_name = "Empleado"

        verbose_name_plural = "Empleados"
    @property
    def antiguedad(self):

        hoy = date.today()

        años = (
            hoy.year
            -
            self.fecha_ingreso.year
        )

        if (
            (hoy.month, hoy.day)
            <
            (
                self.fecha_ingreso.month,
                self.fecha_ingreso.day
            )
        ):

            años -= 1

        return años
    def __str__(self):

        return self.nombre_completo