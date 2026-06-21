from django.conf import settings
from django.db import models


class HistorialCambio(models.Model):

    MODULO_CHOICES = [
        ("LOGIN", "Login"),
        ("LOGOUT", "Logout"),
        ("EMPLEADOS", "Empleados"),
        ("PLANILLAS", "Planillas"),
        ("PDF", "PDF"),
        ("PRODUCTOS", "Productos"),
        ("COMPRAS", "Compras"),
        ("VENTAS", "Ventas"),
        ("ASISTENCIAS", "Asistencias"),
        ("AUSENCIAS", "Ausencias"),
        ("CONFIGURACION", "Configuración"),
        ("SISTEMA", "Sistema"),
    ]

    ACCION_CHOICES = [
        ("CREAR", "Crear"),
        ("EDITAR", "Editar"),
        ("ELIMINAR", "Eliminar"),
        ("GENERAR", "Generar"),
        ("DESCARGAR", "Descargar"),
        ("LOGIN", "Login"),
        ("LOGOUT", "Logout"),
        ("REGISTRAR", "Registrar"),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    modulo = models.CharField(
        max_length=30,
        choices=MODULO_CHOICES
    )

    accion = models.CharField(
        max_length=30,
        choices=ACCION_CHOICES
    )

    descripcion = models.TextField()

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            "-fecha"
        ]

    def __str__(self):

        return f"{self.modulo} - {self.accion}"