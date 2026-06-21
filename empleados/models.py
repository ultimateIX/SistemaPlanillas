from django.db import models


class Empleado(models.Model):

    TIPO_CONTRATO_CHOICES = [
        ("INDEFINIDO", "Indefinido"),
        ("TEMPORAL", "Temporal"),
        ("SERVICIOS", "Servicios profesionales"),
        ("MEDIO_TIEMPO", "Medio tiempo"),
    ]

    JORNADA_CHOICES = [
        ("TIEMPO_COMPLETO", "Tiempo completo"),
        ("MEDIO_TIEMPO", "Medio tiempo"),
        ("POR_HORAS", "Por horas"),
    ]

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

    tipo_contrato = models.CharField(
        max_length=30,
        choices=TIPO_CONTRATO_CHOICES,
        default="INDEFINIDO"
    )

    fecha_inicio_contrato = models.DateField(
        null=True,
        blank=True
    )

    fecha_fin_contrato = models.DateField(
        null=True,
        blank=True
    )

    jornada = models.CharField(
        max_length=30,
        choices=JORNADA_CHOICES,
        default="TIEMPO_COMPLETO"
    )

    activo = models.BooleanField(
        default=True
    )

    class Meta:

        ordering = [
            "nombre_completo"
        ]

    def __str__(self):

        return self.nombre_completo